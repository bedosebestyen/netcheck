import asyncio
from chcker import check_tcp, check_icmp
import logging
import sys
import random

"""
TODO: Test on linux, cli could be deleted, other protocols in chcker, implement some success ratio
        make the code more readable/cleaner, implementing SO_MARK, implementing scripts for IP pool,
        when there is an exception script pauses a little need to know why exactly, timeouts needs streamlining
"""

source = "/var/lib/top-1000-domains/hungary"

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(sys.stdout),
                        logging.FileHandler("base_log", mode="w")
                    ])

def hosts_from_file(source):
    with open(source, 'r') as file:
        hosts = [line.strip() for line in file]
    return hosts

notreachable_hosts = set()

hosts = hosts_from_file(source)

def random_host(notreachable_hosts, hosts):
    # Take out the unreachable hosts from the hosts list, then return a random host from them.
    reachable_hosts = [host for host in hosts if host not in notreachable_hosts]
    #gives back the first element of a 1 long list
    return random.sample(reachable_hosts, 1)[0]



weights = {
        check_icmp: 1,
        check_tcp : 1
    }




def weighted_run(weights, task_args):
    # Iterate through the key value pairs of the dictionary(weight=weight, test = check_icmp...)
    # Call the function associated with each test, _ placeholder
    # Return a list with the tasks
    return [task_args[test]() for test, weight in weights.items() for _ in range(weight)]

#needs to streamline main() too chaotic as it is
async def main() -> None:
    #Pick random host from reachable
    rnd_host = random_host(notreachable_hosts, hosts)
    
    
    """
    Lambda is used here because you want to assign the function object itself
    not the result of the function call. It creates and returns the tests.
"""
    task_args = {
    check_icmp: lambda: asyncio.create_task(check_icmp(rnd_host, 2)),
    check_tcp: lambda: asyncio.create_task(check_tcp(rnd_host, 80, 2))
    }
    # Create a list of tasks
    tasks = weighted_run(weights, task_args)
    
    # with .as_completed as soon as a task is finished we can work with the result, .gather maybe better will test later
    for task in asyncio.as_completed(tasks):
        try:
            #wait for a task to finish
            results = await asyncio.gather(*tasks)
            for result in results:
                if not result:
                    notreachable_hosts.add(rnd_host)
        except Exception as e:
            logging.error(f'An exception occurred during the checks: {e}')
            notreachable_hosts.add(rnd_host)
    logging.info(notreachable_hosts)
        
    
if __name__ == '__main__':
    try:
        while True:
            try:
                asyncio.run(main())
            except Exception as e:
                logging.error(f"An error occured during __main__: {e}")
                sys.exit()
    except KeyboardInterrupt:
        #Stop when ctrl + c or ctrl + z is pressed
        logging.info("Exiting the program...")
