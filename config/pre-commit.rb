require 'fileutils'

raw_path = 'sample_raw/'
target_path = 'sample/'

count = 0

ARGV.all? do |filepath|
    next filepath if filepath.match(/^sample\//)
    next filepath if File.extname(filepath) != '.py'

    path = filepath.dup
    path.slice!(raw_path)

    # make clean source
    src_file = File.open(filepath, 'r')
    dest_file = File.open(target_path + path, 'w')
    src_file.each_line do |line|
        next line if /^\s*\/\/! \[.*\]/ =~ line
        dest_file.puts(line)
    end
    count += 1
end

exit count == 0 ? 0 : 1
