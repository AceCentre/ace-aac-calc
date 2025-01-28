import click
from .calculator import Calculator

@click.command()
@click.argument('expression', required=False)
@click.option('--readpasteboard', is_flag=True, help='Watch pasteboard for calculations')
@click.option('--output-to-pasteboard', is_flag=True, help='Output result to pasteboard')
@click.option('--return', 'return_format', type=click.Choice(['answer', 'answer,calc', 'full']), 
              default='full', help='Format of the output')
def main(expression, readpasteboard, output_to_pasteboard, return_format):
    """Scientific Calculator CLI for AAC users."""
    calc = Calculator()
    
    if readpasteboard:
        if output_to_pasteboard:
            click.echo("Error: Cannot use --output-to-pasteboard with --readpasteboard", err=True)
            return
        
        # Define callback for pasteboard updates
        def on_result(result, expression):
            click.echo(calc.format_output(result, return_format))
            
        calc.watch_pasteboard(callback=on_result)
        return
    
    if not expression:
        click.echo("Error: Expression required when not in pasteboard mode", err=True)
        return
    
    try:
        result = calc.evaluate(expression)
        
        # Format output
        output = calc.format_output(result, return_format)
        
        # Handle output
        if output_to_pasteboard:
            calc.output_to_pasteboard(result, return_format)
        
        click.echo(output)
        
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True) 