import click
from scicalc.calculator import Calculator
import pyperclip

@click.command()
@click.argument('expression', required=False)
@click.option('--readpasteboard', is_flag=True, help='Watch pasteboard for calculations')
@click.option('--readpasteboard-once', is_flag=True, help='Read and calculate one expression from pasteboard')
@click.option('--output-to-pasteboard', is_flag=True, help='Output result to pasteboard instead of stdout')
@click.option('--return', 'return_format', type=click.Choice(['answer', 'answer,calc', 'full']), 
              default='full', help='Format of the output')
def main(expression, readpasteboard, readpasteboard_once, output_to_pasteboard, return_format):
    """Scientific Calculator CLI for AAC users."""
    calc = Calculator()
    
    if readpasteboard and readpasteboard_once:
        raise click.UsageError("Cannot use both --readpasteboard and --readpasteboard-once")
    
    if readpasteboard:
        if output_to_pasteboard:
            raise click.UsageError("Cannot use --output-to-pasteboard with --readpasteboard")
        if expression:
            raise click.UsageError("Cannot provide expression with --readpasteboard")
        calc.watch_pasteboard()
        return
    
    if readpasteboard_once:
        expression = pyperclip.paste().strip()
        if not expression:
            raise click.UsageError("No expression found in pasteboard")
    
    if not expression and not readpasteboard_once:
        raise click.UsageError("Please provide an expression or use --readpasteboard")
    
    try:
        result = calc.evaluate(expression)
        
        # Format output
        output = calc.format_output(result, return_format)
        
        # Handle output
        if output_to_pasteboard:
            pyperclip.copy(output)
        else:
            click.echo(output)
        
    except ValueError as e:
        raise click.UsageError(str(e)) 