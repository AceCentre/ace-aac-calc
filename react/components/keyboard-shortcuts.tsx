import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { HelpCircle } from "lucide-react"

export function KeyboardShortcuts() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="ghost" size="icon" className="h-8 w-8" aria-label="Keyboard Shortcuts">
          <HelpCircle className="h-4 w-4" />
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Keyboard Shortcuts</DialogTitle>
          <DialogDescription>Available keyboard shortcuts for the calculator</DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-2 items-center gap-4">
            <div className="space-y-4">
              <h3 className="font-medium">Expression Entry</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span>Move to Previous Expression</span>
                  <kbd className="rounded bg-muted px-2 py-0.5">↑</kbd>
                </div>
                <div className="flex justify-between">
                  <span>Move to Next Expression</span>
                  <kbd className="rounded bg-muted px-2 py-0.5">↓</kbd>
                </div>
                <div className="flex justify-between">
                  <span>Evaluate Expression</span>
                  <kbd className="rounded bg-muted px-2 py-0.5">Enter</kbd>
                </div>
                <div className="flex justify-between">
                  <span>Toggle Degrees/Radians</span>
                  <kbd className="rounded bg-muted px-2 py-0.5">Alt + D</kbd>
                </div>
                <div className="flex justify-between">
                  <span>Copy Highlighted Expression</span>
                  <kbd className="rounded bg-muted px-2 py-0.5">Ctrl/Cmd + C</kbd>
                </div>
              </div>
            </div>
            <div className="space-y-4">
              <h3 className="font-medium">Memory Operations</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span>Memory Plus (M+)</span>
                  <kbd className="rounded bg-muted px-2 py-0.5">Ctrl + P</kbd>
                </div>
                <div className="flex justify-between">
                  <span>Memory Minus (M-)</span>
                  <kbd className="rounded bg-muted px-2 py-0.5">Ctrl + M</kbd>
                </div>
                <div className="flex justify-between">
                  <span>Memory Recall (MR)</span>
                  <kbd className="rounded bg-muted px-2 py-0.5">Ctrl + R</kbd>
                </div>
              </div>
            </div>
          </div>
          <div className="space-y-4">
            <h3 className="font-medium">Special Characters</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span>Fraction</span>
                  <kbd className="rounded bg-muted px-2 py-0.5">/</kbd>
                </div>
                <div className="flex justify-between">
                  <span>Multiplication</span>
                  <kbd className="rounded bg-muted px-2 py-0.5">*</kbd>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span>Exponent</span>
                  <kbd className="rounded bg-muted px-2 py-0.5">^</kbd>
                </div>
                <div className="flex justify-between">
                  <span>Square Root</span>
                  <kbd className="rounded bg-muted px-2 py-0.5">sqrt()</kbd>
                </div>
              </div>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
