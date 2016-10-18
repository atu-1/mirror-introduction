require 'fileutils'

src_path = 'sample_raw/'
dest_path = 'sample/'

ARGV.all? do |filepath|
    if File.extname(filepath) == '.py' then
        path = filepath.dup
        path.slice!(src_path)
        src_file = File.open(filepath, 'r')
        dest_file = File.open(dest_path + path, 'w')
        src_file.each_line do |line|
            next line if /^\s*\/\/! \[.*\]/ =~ line
            dest_file.puts(line)
        end
    end
end

exit 0
