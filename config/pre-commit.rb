require 'fileutils'

src_path = 'sample_raw/'
dest_path = 'sample/'

ARGV.all? do |filepath|
    if File.extname(filepath) == '.py' then
        path = filepath.dup
        path.slice!(/^\s*\/\/! \[.*\]/);
        print path
        #FileUtils.cp(filepath, dest_path + File.basename(filepath))
        o
    end
end

exit 0
