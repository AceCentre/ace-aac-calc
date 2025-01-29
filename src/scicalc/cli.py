import click
from scicalc.calculator import Calculator
import pyperclip
import logging
import os
import sys

def setup_logging():
    """Setup logging to both file and console"""
    print("Setting up logging...")  # Direct console output for debugging
    
    # Get script location
    if getattr(sys, 'frozen', False):
        # PyInstaller executable
        print(f"Running as PyInstaller executable: {sys.executable}")
        script_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'AAC Tools', 'Scientific Calculator')
    else:
        # Running from source
        print("Running from source")
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print(f"Script directory: {script_dir}")
    log_dir = os.path.join(script_dir, 'logs')
    print(f"Log directory: {log_dir}")
    
    try:
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'scicalc.log')
        print(f"Attempting to write to log file: {log_file}")
        
        # Test write access
        with open(log_file, 'a') as f:
            f.write("Log file initialized\n")
        
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)  # Explicitly use stdout
            ]
        )
        print("Logging setup complete")
        logging.info(f"Logging to: {log_file}")
        
    except Exception as e:
        print(f"Error setting up logging: {str(e)}")
        # Fall back to temp directory if we can't write to preferred location
        import tempfile
        temp_dir = tempfile.gettempdir()
        print(f"Falling back to temp directory: {temp_dir}")
        log_dir = os.path.join(temp_dir, 'AAC Tools', 'Scientific Calculator', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'scicalc.log')
        
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)  # Explicitly use stdout
            ]
        )
        print(f"Logging setup complete (using temp directory)")
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

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import traceback
        with open('error.log', 'w') as f:
            f.write(f"Error: {str(e)}\n")
            f.write(traceback.format_exc())
        raise 