import click
from scicalc.calculator import Calculator
import pyperclip
import logging
import os
import sys

def setup_logging():
    """Setup logging to both file and console"""
    # Get script location
    if getattr(sys, 'frozen', False):
        # PyInstaller executable
        script_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'AAC Tools', 'Scientific Calculator')
    else:
        # Running from source
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
    log_dir = os.path.join(script_dir, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'scicalc.log')
    
    # Ensure we can write to the log file
    try:
        with open(log_file, 'a') as f:
            pass
    except:
        # Fall back to temp directory if we can't write to preferred location
        import tempfile
        log_dir = os.path.join(tempfile.gettempdir(), 'AAC Tools', 'Scientific Calculator', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'scicalc.log')

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    logging.info(f"Logging to: {log_file}")

@click.command()
@click.argument('expression', required=False)
@click.option('--readpasteboard', is_flag=True, help='Watch pasteboard for calculations')
@click.option('--readpasteboard-once', is_flag=True, help='Read and calculate one expression from pasteboard')
@click.option('--output-to-pasteboard', is_flag=True, help='Output result to pasteboard instead of stdout')
@click.option('--return', 'return_format', type=click.Choice(['answer', 'answer,calc', 'full']), 
              default='full', help='Format of the output')
def main(expression, readpasteboard, readpasteboard_once, output_to_pasteboard, return_format):
    """Scientific Calculator CLI for AAC users."""
    setup_logging()
    logging.info("Starting Scientific Calculator")
    logging.debug(f"Args: expression={expression}, readpasteboard={readpasteboard}, "
                 f"readpasteboard_once={readpasteboard_once}, output_to_pasteboard={output_to_pasteboard}, "
                 f"return_format={return_format}")
    
    calc = Calculator()
    
    if readpasteboard and readpasteboard_once:
        logging.error("Cannot use both --readpasteboard and --readpasteboard-once")
        raise click.UsageError("Cannot use both --readpasteboard and --readpasteboard-once")
    
    if readpasteboard:
        if output_to_pasteboard:
            logging.error("Cannot use --output-to-pasteboard with --readpasteboard")
            raise click.UsageError("Cannot use --output-to-pasteboard with --readpasteboard")
        if expression:
            logging.error("Cannot provide expression with --readpasteboard")
            raise click.UsageError("Cannot provide expression with --readpasteboard")
        logging.info("Starting pasteboard watch mode")
        calc.watch_pasteboard()
        return
    
    if readpasteboard_once:
        expression = pyperclip.paste().strip()
        logging.debug(f"Read from pasteboard: {expression}")
        if not expression:
            logging.error("No expression found in pasteboard")
            raise click.UsageError("No expression found in pasteboard")
    
    if not expression and not readpasteboard_once:
        logging.error("No expression provided")
        raise click.UsageError("Please provide an expression or use --readpasteboard")
    
    try:
        logging.debug(f"Evaluating expression: {expression}")
        result = calc.evaluate(expression)
        logging.debug(f"Result: {result}")
        
        # Format output
        output = calc.format_output(result, return_format)
        logging.debug(f"Formatted output: {output}")
        
        # Handle output
        if output_to_pasteboard:
            logging.info("Copying result to pasteboard")
            pyperclip.copy(output)
        else:
            logging.info("Outputting result to stdout")
            click.echo(output)
        
    except ValueError as e:
        logging.error(f"Error evaluating expression: {str(e)}")
        raise click.UsageError(str(e)) 