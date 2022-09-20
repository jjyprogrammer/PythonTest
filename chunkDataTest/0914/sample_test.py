import os, sys, subprocess, shutil, argparse


current_dir = os.path.split(os.path.realpath(__file__))[0]
root_path = os.path.join(current_dir, "..")
root_path = os.path.normpath(root_path)
print("current path: %s" % (current_dir))
print("root_path: %s" % (root_path))
open_log = True
region = ""
skip_unzip = False
temp_settings = True
network = True
global_data_path = "/data/dyuan/data"

def getRegionFromDirName(name) :
    if name.startswith("NA") :
        return "NA"
    elif name.startswith("EU") :
        return "EU"
    elif name.startswith("ANZ") :
        return "ANZ"

def getRegionMapDirNames(region) :
    global root_path
    region_dir_names = {}
    data_path = os.path.join(root_path, "data")
    print("data_path: %s" % (data_path))
    dirs = os.listdir(data_path)
    
    for dir in dirs :
        if region :
            if dir.startswith(region) :
                return {region : dir}
        else :
            region_dir_names[getRegionFromDirName(dir)] = dir
    return region_dir_names

def chmodSh() :
    global root_path
    ret_list = []
    data_path = os.path.join(root_path, "data")
    print("data_path: %s" % (data_path))
    dirs = os.listdir(data_path);
    for dir in dirs :
        region_version_list = dir.split("_")
        print("region : %s , version : %s " % (region_version_list[0], region_version_list[1]))
        ret_list.append(region_version_list)
        region_path = os.path.join(data_path, dir) 
        sub_dirs = os.listdir(region_path)
        for sub_dir in sub_dirs :
            sub_dir_path = os.path.join(region_path, sub_dir)
            sh_file_path = os.path.join(sub_dir_path, "symlink_linux.sh")
            if os.path.exists(sh_file_path) :
                cmd = "chmod 777 %s" % (sh_file_path)
                print("run cmd : %s" % cmd)
                cmd = cmd.split()
                subprocess.check_call(cmd)           

def doSampleTest() :
    global region
    modifyCommonConfiguration(getConfigurationPath())
    chmodExecute(getExecutePath())
    settings_paths = modifySettings()
    if temp_settings :
        runSampleTestCommand(getLibPath(), getExecutePath(), settings_paths)
    else :
        runSampleTestCommand(getLibPath(), getExecutePath(), getSettingsPath(region))

def modifySettings() :
    global region
    global global_data_path
    settings_paths = []
    bin_path = getBinPath()
    configuration_path = getConfigurationPath()
    region_dirs = getRegionMapDirNames(region)
    if not region_dirs :
        raise Exception("can't get region with dir name")
    print(region_dirs)
    for region_key in region_dirs :
        temp_settings_path = os.path.join(bin_path, "settingsPath_%s_temp.ini" % region_key)
        settings_paths.append(temp_settings_path)
        if region_key == "NA" :
            with open(temp_settings_path, 'w') as write_file :
                write_file.write(region_key + "\n")
                write_file.write(bin_path + "\n")
                write_file.write(configuration_path + "\n")
                write_file.write("true" + "\n")
                write_file.write("\n")
                write_file.write("com.telenav.telenav_maps_na_common|{1}/{0}/NA_Common\ncom.telenav.telenav_maps_na_canada|{1}/{0}/NA_Canada\ncom.telenav.telenav_maps_na_us_west|{1}/{0}/NA_US_West\ncom.telenav.telenav_maps_na_mexico|{1}/{0}/NA_Mexico\ncom.telenav.telenav_maps_na_us_central|{1}/{0}/NA_US_Central\ncom.telenav.telenav_maps_na_us_north_mid|{1}/{0}/NA_US_North_Mid\ncom.telenav.telenav_maps_na_us_north_east|{1}/{0}/NA_US_North_East\ncom.telenav.telenav_maps_na_us_south_east|{1}/{0}/NA_US_South_East".format(region_dirs[region_key], global_data_path))
        elif region_key == "EU" :
            with open(temp_settings_path, 'w') as write_file :
                write_file.write(region_key + "\n")
                write_file.write(bin_path + "\n")
                write_file.write(configuration_path + "\n")
                write_file.write("true" + "\n")
                write_file.write("\n")
                write_file.write("com.telenav.telenav_maps_eu_common|{1}/{0}/EU_Common\ncom.telenav.telenav_maps_eu_north_uk|{1}/{0}/EU_North_Uk\ncom.telenav.telenav_maps_eu_gps|{1}/{0}/EU_Gps\ncom.telenav.telenav_maps_eu_france|{1}/{0}/EU_France\ncom.telenav.telenav_maps_eu_central|{1}/{0}/EU_Central\ncom.telenav.telenav_maps_eu_south|{1}/{0}/EU_South\ncom.telenav.telenav_maps_eu_east|{1}/{0}/EU_East\ncom.telenav.telenav_maps_eu_cyprus|{1}/{0}/EU_Cyprus".format(region_dirs[region_key], global_data_path))
        elif region_key == "ANZ" :
            with open(temp_settings_path, 'w') as write_file :
                write_file.write(region_key + "\n")
                write_file.write(bin_path + "\n")
                write_file.write(configuration_path + "\n")
                write_file.write("true" + "\n")
                write_file.write("\n")
                write_file.write("fulldata|{1}/{0}".format(region_dirs[region_key], global_data_path))
    return settings_paths;  

def chmodExecute(execute_path) :
    cmd = "chmod +x %s" % (execute_path)
    print("run cmd : %s" % cmd)
    subprocess.check_call(cmd.split())
    
def getSettingsPath(region) :
    paths = []
    if region :
        if region == "NA" :
            paths.append(getSettingsPathNA())
        elif region == "EU" :
            paths.append(getSettingsPathEU())
    else :
        regions = getRegionMapDirNames(region).keys()
        for region in regions :
            if region == "NA" :
                paths.append(getSettingsPathNA())
            elif region == "EU" :
                paths.append(getSettingsPathEU())
    return paths

def runSampleTestCommand(lib_path, execute_path, settings_paths) :
    for settings_path in settings_paths :
        cmd = "LD_LIBRARY_PATH=%s %s %s" % (lib_path, execute_path, settings_path)
        print("run cmd : %s" % cmd)
        subprocess.check_call(cmd, shell=True)

def getLibPath() :
    global current_dir
    lib_path = os.path.join(current_dir, "lib")
    if not os.path.exists(lib_path) :
        raise Exception(lib_path + " not exists")
    return lib_path

def getBinPath() :
    global current_dir
    bin_path = os.path.join(current_dir, "samplecode", "bin")
    if not os.path.exists(bin_path) :
        raise Exception(bin_path + " not exists")
    return bin_path

def getSettingsPathEU() :
    bin_path = getBinPath()
    eu_path = os.path.join(bin_path, "settingsPath_EU.ini")
    if not os.path.exists(eu_path) :
        raise Exception(eu_path + " not exists")
    return eu_path

def getSettingsPathNA() :
    bin_path = getBinPath()
    na_path = os.path.join(bin_path, "settingsPath_NA.ini")
    if not os.path.exists(na_path) :
        raise Exception(na_path + " not exists")
    return na_path

def getExecutePath() :
    global current_dir
    execute_path = os.path.join(current_dir, "samplecode", "bin", "run_integrate_tnehp")
    if not os.path.exists(execute_path) :
        raise Exception(execute_path + " not exists")
    return execute_path

def getConfigurationPath() :
    global current_dir
    configuration_path = os.path.join(current_dir, "configuration")
    if not os.path.exists(configuration_path) :
        raise Exception(configuration_path + " not exists")
    return configuration_path

def unzipFile() :
    global current_dir
    for root, dirs, files in os.walk(current_dir, topdown=False):
        for name in files:
            if(name.endswith("sampleapp.zip")) :
                sample_file_path = os.path.join(current_dir, name)
                cmd = "unzip -q -o -d %s %s" % (current_dir, sample_file_path)
                print("run cmd : %s" % cmd)
                cmd = cmd.split()
                subprocess.check_call(cmd)
def modifyCommonConfiguration(configuration_path) :
    global open_log
    contain_network = False
    common_configuration_file = os.path.join(configuration_path, "common_configuration.ini")
    common_configuration_file_new = os.path.join(configuration_path, "common_configuration.ini.new")
    if not os.path.exists(configuration_path) :
        raise Exception(common_configuration_file + " not exists")
    with open(common_configuration_file, 'r') as read_file :
        with open(common_configuration_file_new, 'w') as write_file :
            lines = read_file.readlines()
            for line in lines :
                if line.startswith("TncOUTPUT_TO_FILE") :
                    if open_log :
                        new_log_file_configuration = "TncOUTPUT_TO_FILE = 1" + "\n"
                        write_file.write(new_log_file_configuration)
                else :
                    write_file.write(line)
                if(line.startswith("TcnDEFAULT_NETWORK_STATUS")) :
                    contain_network = True
            if not contain_network and network:
                write_file.write("TcnDEFAULT_NETWORK_STATUS = 0" + "\n")
                write_file.write("TncNEED_VERIFY_TOKEN = 0" + "\n")
    common_configuration_file_backup = common_configuration_file + "_backup"
    shutil.move(common_configuration_file, common_configuration_file_backup)
    shutil.move(common_configuration_file_new, common_configuration_file)
                

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--no-log', required = False, action = 'store_true')
    parser.add_argument('--skip-unzip', required = False, action = 'store_true')
    parser.add_argument('--no-temp-settings', required = False, action = 'store_true')
    parser.add_argument('--no-streaming', required = False, action = 'store_true')
    parser.add_argument('-region', required = False, type = str)
    args = parser.parse_args()
    open_log = not args.no_log
    skip_unzip = args.skip_unzip
    temp_settings = not args.no_temp_settings
    network = not args.no_streaming
    region = args.region
    print("open_log %s" % open_log)
    print("skip_unzip %s" % skip_unzip)
    print("temp_settings %s" % temp_settings)
    print("streaming %s" % network)
    print("region %s" % region)
    chmodSh()
    if not skip_unzip :
        unzipFile()
    doSampleTest()