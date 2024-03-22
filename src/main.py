import argparse
import scraper, plotter
import os

def parse_args():
    parser = argparse.ArgumentParser(description='Autoprice program - standvirtual scraper')
    # Two subcommands: scrape and plot
    subparsers = parser.add_subparsers(dest='command', required=True)
    # Scrape subcommand
    scrape_parser = subparsers.add_parser('pull', help='Pull data from standvirtual')
    scrape_parser.add_argument('brand', type=str, help='Car brand')
    scrape_parser.add_argument('model', type=str, help='Car model')
    scrape_parser.add_argument('--no-headless', action='store_true', help='Run in non-headless mode')
    scrape_parser.add_argument('--pages', type=int, default=9, help='Number of pages to scrape')
    # List subcommand
    list_parser = subparsers.add_parser('list', help='List pulled cars')
    # Plot subcommand
    plot_parser = subparsers.add_parser('plot', help='Plot pulled car data')
    plot_parser.add_argument('filenames', type=str, nargs='+', help='List of filenames for cars')
    plot_parser.add_argument('--no-headless', action='store_true', help='Run in non-headless mode')
    # Scrape and plot subcommand
    run_parser = subparsers.add_parser('run', help='Scrape and plot car data. If car is already scraped, it will be plotted. If not, it will be scraped and then plotted')
    run_parser.add_argument('--no-headless', action='store_true', help='Run in non-headless mode')
    run_parser.add_argument('--pages', type=int, default=9, help='Number of pages to scrape')
    
    args = parser.parse_args()

    if args.command == 'pull':
        print(args)
        scraper.scrape_and_serialize(args.brand.lower(), args.model.lower(), not args.no_headless, args.pages)

    if args.command == 'plot':
        plotter.plot(not args.no_headless, args.filenames)

    if args.command == 'list':
        for file in os.listdir("pickles"):
            print("pickles/"+file)

    if args.command == 'run':
        # Ask user for brand and model until user does not want more

        paths = []
        while True:
            brand = input("Brand: ")
            model = input("Model: ")
            path = "pickles/"+brand.lower()+"-"+model.lower()+".pkl"
            paths.append(path)
            if not os.path.exists(path):
                scraper.scrape_and_serialize(brand.lower(), model.lower(), not args.no_headless, args.pages)
            if input("Do you want to scrape another car? [Y/n] ") == "n":
                break
        #Plot the cars
        plotter.plot(not args.no_headless, paths)


if __name__ == "__main__":
    args = parse_args()
