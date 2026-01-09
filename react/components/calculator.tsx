"use client"

import { useState, useRef, useEffect, useMemo } from "react"
import katex from "katex"
import "katex/dist/katex.min.css"
import { toLatex, evaluateExpression, previewEvaluate } from "@/lib/math-utils"
import { KeyboardShortcuts } from "./keyboard-shortcuts"
import { Button } from "@/components/ui/button"
import debounce from "lodash/debounce"

// Add after imports
const styles = `
  .katex-container .katex {
    text-align: left;
  }
  .katex-container .katex-display {
    text-align: left;
    margin: 0;
  }
`

interface Expression {
  input: string
  result: string
  latex: string
  isError?: boolean
}

interface BracketPreview {
  text: string
  position: number
}

export function Calculator() {
  const [expressions, setExpressions] = useState<Expression[]>([{ input: "", result: "", latex: "", isError: false }])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [memory, setMemory] = useState(0)
  const [isRadians, setIsRadians] = useState(false)
  const [bracketPreview, setBracketPreview] = useState<BracketPreview | null>(null)
  const [latexPreview, setLatexPreview] = useState<string>("")
  const inputRef = useRef<HTMLTextAreaElement>(null)
  const previewRef = useRef<HTMLDivElement>(null)

  // Debounced LaTeX conversion with increased timeout
  const debouncedLatexUpdate = useMemo(
    () =>
      debounce((input: string) => {
        try {
          if (!input.trim()) {
            setLatexPreview("")
            return
          }

          // Try to get a preview result
          const previewResult = previewEvaluate(input, isRadians)
          if (previewResult !== null) {
            setLatexPreview(`${input} = ${previewResult}`)
            return
          }

          // If no preview result, just show the input
          const latex = toLatex(input)
          setLatexPreview(
            latex === input
              ? input
              : katex.renderToString(latex, {
                  throwOnError: false,
                  displayMode: false,
                  strict: false,
                  trust: true,
                }),
          )
        } catch (error) {
          console.error("LaTeX preview error:", error)
          setLatexPreview(input)
        }
      }, 300),
    [isRadians],
  )

  // Update bracket preview when input changes
  const updateBracketPreview = (input: string, cursorPosition: number) => {
    const stack: { char: string; pos: number }[] = []
    const brackets = { "(": ")", "[": "]", "{": "}" }
    let missingClosing = ""

    // Analyze up to cursor position
    for (let i = 0; i < cursorPosition; i++) {
      const char = input[i]
      if ("([{".includes(char)) {
        stack.push({ char, pos: i })
      } else if (")]}".includes(char)) {
        if (stack.length > 0 && brackets[stack[stack.length - 1].char as keyof typeof brackets] === char) {
          stack.pop()
        }
      }
    }

    // Build preview text
    if (stack.length > 0) {
      missingClosing = stack
        .map(({ char }) => brackets[char as keyof typeof brackets])
        .reverse()
        .join("")
      setBracketPreview({ text: missingClosing, position: cursorPosition })
    } else {
      setBracketPreview(null)
    }
  }

  // Update preview position when cursor moves
  useEffect(() => {
    const updatePreviewPosition = () => {
      if (!inputRef.current || !previewRef.current || !bracketPreview) return

      const input = inputRef.current
      const preview = previewRef.current

      // Get the text content up to the cursor
      const textBeforeCursor = input.value.substring(0, input.selectionStart)

      // Create a temporary span to measure the text width
      const span = document.createElement("span")
      span.style.font = window.getComputedStyle(input).font
      span.style.visibility = "hidden"
      span.style.position = "absolute"
      span.textContent = textBeforeCursor
      document.body.appendChild(span)

      // Calculate position
      const textWidth = span.offsetWidth

      // Position the preview
      preview.style.left = `${textWidth + input.offsetLeft + 8}px`
      preview.style.top = `${input.offsetTop + 8}px`

      document.body.removeChild(span)
    }

    const debouncedUpdatePosition = debounce(updatePreviewPosition, 16) // Debounce to 60fps

    const events = ["select", "click", "keyup"]
    events.forEach((event) => {
      inputRef.current?.addEventListener(event, debouncedUpdatePosition)
    })

    return () => {
      events.forEach((event) => {
        inputRef.current?.removeEventListener(event, debouncedUpdatePosition)
      })
      debouncedUpdatePosition.cancel()
    }
  }, [bracketPreview])

  // Clean up debounce on unmount
  useEffect(() => {
    return () => {
      debouncedLatexUpdate.cancel()
    }
  }, [debouncedLatexUpdate])

  // Handle keyboard shortcuts
  useEffect(() => {
    const getExpressionCopyText = (exp: Expression) => {
      if (!exp.input) return ""
      if (exp.isError) return exp.result || exp.input
      if (exp.result) {
        return exp.result
      }
      return exp.input
    }

    const getExpressionFullCopyText = (exp: Expression) => {
      if (!exp.input) return ""
      if (exp.isError) return exp.result || exp.input
      if (exp.result && !exp.input.includes("=") && !/^[a-zA-Z\s]+$/.test(exp.input)) {
        return `${exp.input} = ${exp.result}`
      }
      return exp.input
    }

    const copyToClipboard = async (text: string) => {
      if (!text) return
      try {
        await navigator.clipboard.writeText(text)
      } catch (error) {
        const textarea = document.createElement("textarea")
        textarea.value = text
        textarea.setAttribute("readonly", "true")
        textarea.style.position = "absolute"
        textarea.style.left = "-9999px"
        document.body.appendChild(textarea)
        textarea.select()
        document.execCommand("copy")
        document.body.removeChild(textarea)
      }
    }

    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.key === "Enter" || e.key === "Return") && !e.shiftKey) {
        e.preventDefault()
        evaluate()
      } else if (e.key === "Escape") {
        e.preventDefault()
        clearWorkpad()
        return
      } else if (e.key === "ArrowUp") {
        e.preventDefault()
        setCurrentIndex((prev) => Math.max(0, prev - 1))
      } else if (e.key === "ArrowDown") {
        e.preventDefault()
        setCurrentIndex((prev) => Math.min(expressions.length - 1, prev + 1))
      }

      // Toggle between degrees and radians
      if ((e.altKey || e.metaKey) && e.key.toLowerCase() === "d") {
        e.preventDefault()
        setIsRadians((prev) => !prev)
      }

      // Memory operations
      if (e.ctrlKey || e.metaKey) {
        const key = e.key.toLowerCase()
        if (key === "c" || (key === "l" && e.shiftKey)) {
          const selection = window.getSelection()?.toString() ?? ""
          const activeElement = document.activeElement
          const activeInputElement =
            activeElement instanceof HTMLInputElement || activeElement instanceof HTMLTextAreaElement
              ? activeElement
              : null
          const inputSelectionEmpty =
            !activeInputElement ||
            activeInputElement.selectionStart === null ||
            activeInputElement.selectionEnd === null ||
            activeInputElement.selectionStart === activeInputElement.selectionEnd

          if (!selection && inputSelectionEmpty) {
            const text =
              key === "l" && e.shiftKey
                ? getExpressionFullCopyText(expressions[currentIndex])
                : getExpressionCopyText(expressions[currentIndex])
            if (text) {
              e.preventDefault()
              copyToClipboard(text)
            }
          }
          return
        }
        switch (e.key) {
          case "p":
            e.preventDefault()
            memoryPlus()
            break
          case "m":
            e.preventDefault()
            memoryMinus()
            break
          case "r":
            e.preventDefault()
            memoryRecall()
            break
        }
      }
    }

    window.addEventListener("keydown", handleKeyDown)
    return () => window.removeEventListener("keydown", handleKeyDown)
  }, [expressions])

  // Memory functions
  const memoryPlus = () => {
    const currentValue = Number.parseFloat(expressions[currentIndex].result) || 0
    setMemory((prev) => prev + currentValue)
  }

  const memoryMinus = () => {
    const currentValue = Number.parseFloat(expressions[currentIndex].result) || 0
    setMemory((prev) => prev - currentValue)
  }

  const memoryRecall = () => {
    const newExpressions = [...expressions]
    newExpressions[currentIndex] = {
      input: memory.toString(),
      result: memory.toString(),
      latex: memory.toString(),
      isError: false,
    }
    setExpressions(newExpressions)
  }

  const clearWorkpad = () => {
    setExpressions([{ input: "", result: "", latex: "", isError: false }])
    setCurrentIndex(0)
  }

  // Evaluate the current expression
  const evaluate = () => {
    const currentExp = expressions[currentIndex]
    if (!currentExp.input.trim()) return

    try {
      // Check if input is just text (only letters and spaces)
      if (/^[a-zA-Z\s]+$/.test(currentExp.input)) {
        const newExpressions = [...expressions]
        newExpressions[currentIndex] = {
          ...currentExp,
          result: currentExp.input,
          latex: currentExp.input,
          isError: false,
        }

        // Add new empty expression and move to it
        newExpressions.push({ input: "", result: "", latex: "", isError: false })
        setExpressions(newExpressions)
        setCurrentIndex(currentIndex + 1)
        return
      }

      // Calculate the result
      const result = evaluateExpression(currentExp.input, isRadians)

      const newExpressions = [...expressions]
      newExpressions[currentIndex] = {
        ...currentExp,
        result: result,
        latex: toLatex(currentExp.input),
        isError: false,
      }

      // Add new empty expression and immediately move to it
      newExpressions.push({ input: "", result: "", latex: "", isError: false })
      setExpressions(newExpressions)
      setCurrentIndex(currentIndex + 1)
    } catch (error) {
      const newExpressions = [...expressions]
      newExpressions[currentIndex] = {
        ...currentExp,
        result: error instanceof Error ? error.message : "Invalid expression",
        isError: true,
      }
      setExpressions(newExpressions)
    }
  }

  useEffect(() => {
    // Insert styles
    const styleSheet = document.createElement("style")
    styleSheet.innerText = styles
    document.head.appendChild(styleSheet)

    return () => {
      document.head.removeChild(styleSheet)
    }
  }, [])

  return (
    <div className="container mx-auto max-w-2xl p-4">
      <div className="relative flex flex-col gap-4 rounded-lg border bg-card p-4 shadow-sm">
        <div className="flex items-center justify-between">
          <Button variant="ghost" size="sm" onClick={() => setIsRadians((prev) => !prev)} className="text-xs">
            {isRadians ? "RAD" : "DEG"}
          </Button>
          <KeyboardShortcuts />
        </div>
        {/* Expression History */}
        <div className="flex flex-col gap-2">
          {expressions.map((exp, index) => (
            <div
              key={index}
              className={`flex flex-col gap-1 border-b border-border p-2 ${
                index === currentIndex ? "bg-accent/50" : ""
              }`}
            >
              {/* Input Expression */}
              {exp.input && (
                <div className="text-left pl-2">
                  {exp.isError ? (
                    <span className="text-destructive">{exp.result}</span>
                  ) : (
                    <div
                      className="katex-container text-left"
                      dangerouslySetInnerHTML={{
                        __html: katex.renderToString(
                          toLatex(exp.input) +
                            // Only add equals and result for non-text expressions
                            (exp.result && !exp.input.includes("=") && !/^[a-zA-Z\s]+$/.test(exp.input)
                              ? ` = ${toLatex(exp.result)}`
                              : ""),
                          {
                            throwOnError: false,
                            displayMode: true,
                            strict: false,
                            trust: true,
                            output: "html",
                            displayMode: false,
                          },
                        ),
                      }}
                    />
                  )}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Input Area */}
        <div className="sticky bottom-0 bg-background p-2">
          <div className="relative">
            <textarea
              ref={inputRef}
              value={expressions[currentIndex].input}
              onChange={(e) => {
                const newExpressions = [...expressions]
                const input = e.target.value
                newExpressions[currentIndex] = {
                  ...newExpressions[currentIndex],
                  input: input,
                }
                setExpressions(newExpressions)
                updateBracketPreview(input, e.target.selectionStart || 0)
                debouncedLatexUpdate(input)
              }}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault()
                  e.stopPropagation()
                  evaluate()
                }
              }}
              onClick={(e) => {
                const target = e.target as HTMLTextAreaElement
                updateBracketPreview(target.value, target.selectionStart || 0)
              }}
              onSelect={(e) => {
                const target = e.target as HTMLTextAreaElement
                updateBracketPreview(target.value, target.selectionStart || 0)
              }}
              className="w-full resize-none rounded-md border-none bg-transparent p-2 font-mono focus:outline-none"
              rows={1}
              placeholder="Enter expression..."
              autoFocus
            />
            {bracketPreview && (
              <div
                ref={previewRef}
                className="pointer-events-none absolute font-mono text-muted-foreground/50"
                style={{ height: "1.5rem", lineHeight: "1.5rem" }}
              >
                {bracketPreview.text}
              </div>
            )}
          </div>
        </div>

        {/* Memory Display */}
        <div className="text-right text-sm text-muted-foreground">{memory !== 0 && `M = ${memory}`}</div>
      </div>
    </div>
  )
}
