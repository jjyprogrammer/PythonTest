import os,sys

data_path = "123"
region_dirs = {"NA":"NA123"};
for region_key in region_dirs :
    print("com.telenav.telenav_maps_na_common|{1}/{0}/NA_Common\ncom.telenav.telenav_maps_na_canada|{1}/{0}/NA_Canada\ncom.telenav.telenav_maps_na_us_west|{1}/{0}/NA_US_West\ncom.telenav.telenav_maps_na_mexico|{1}/{0}/NA_Mexico\ncom.telenav.telenav_maps_na_us_central|{1}/{0}/NA_US_Central\ncom.telenav.telenav_maps_na_us_north_mid|{1}/{0}/NA_US_North_Mid\ncom.telenav.telenav_maps_na_us_north_east|{1}/{0}/NA_US_North_East\ncom.telenav.telenav_maps_na_us_south_east|{1}/{0}/NA_US_South_East".format(region_dirs[region_key], data_path))