
import uploader
import weatherman
import argparse

def main():
    parser = argparse.ArgumentParser('Download from weatherman and upload to wunderground')
    parser.add_argument('-o', '--output', help='filename to store output files', default="")
    parser.add_argument('-s', '--source', help='Weatherman ip address', required=True)
    parser.add_argument('-c', '--config', help='config file to describe output', default='./weatherman2.json')
    
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        print("Getting weather data from " + args.source)
        print("using sourcefile " + args.config)
    
    weather_data = weatherman.weatherman_get_data(args.source, args.config)

    if args.verbose:
        print("Got weather data --")
        print(weather_data)

    if len(args.output) > 0:
        try:
            outfile = open(args.output, "rw")
            outfile.write(weather_data)
            outfile.close()
        except Exception:
            print("Failed to write data to " + args.output)
            return

    station_id = weather_data.pop("id")
    station_key = weather_data.pop("key")
    
    utc_timestamp = weather_data.pop("dateutc")

    if args.verbose:
        print("uploading...")
    uploader.wunderground_upload_data_point(station_id, station_key, weather_data, utc_timestamp)

    print("Uploaded weather data for station ID " + station_id + " UTC: " + utc_timestamp)

if __name__ == "__main__":
    main()
