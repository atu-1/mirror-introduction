require 'fileutils'

dest_path = '_sample/'

ARGV.all? do |filepath|
    if File.extname(filepath) == '.py' then
        FileUtils.cp(filepath, dest_path + File.basename(filepath))
        print filepath
        o
    end
end

exit 0
