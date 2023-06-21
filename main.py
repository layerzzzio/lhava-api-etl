import sys
import importlib
from blockchain import Blockchain
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')


def print_usage():
    print("Usage: python main.py [data_type] [class] [args...]")
    print("Available blockchains: solana, ethereum")
    print("Example: python main.py blockchain Solana Gjx4wAMi7QUriRqXpjKydb2MJ3qzxHX9yeaj4DHQNJnh")


if len(sys.argv) < 3:
    print_usage()
    sys.exit(1)

data_type = sys.argv[1]
class_name = sys.argv[2]
method_args = sys.argv[3:]
blockchain_name = class_name.lower()
module_name = f"{data_type}.{blockchain_name}.{blockchain_name}"

try:
    module = importlib.import_module(module_name)
    blockchain_class = getattr(module, class_name)

    if not issubclass(blockchain_class, Blockchain):
        raise TypeError(f"{class_name} must be a subclass of Blockchain")

    blockchain_instance = blockchain_class()

    logging.info('1) EXTRACT')
    blockchain_instance.extract(method_args[0])

    logging.info('2) TRANSFORM')
    df = blockchain_instance.transform()

    logging.info('3) LOAD')
    blockchain_instance.load(df)

except ImportError:
    print(f"Error importing module: {module_name}")
    print_usage()
    sys.exit(1)

except (AttributeError, TypeError) as e:
    print(f"Error instantiating module class or providing incorrect arguments: {str(e)}")
    sys.exit(1)

except Exception as e:
    print(f"An error occurred: {str(e)}")
