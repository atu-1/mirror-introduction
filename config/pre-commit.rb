require 'fileutils'

src_path = '_sample/'

print 'aa'

ARGV.all? do |filename|
    print filename
    if File.extname(filename) == '.py' then
        FileUtils.cp(filename, dest + filename)
        print filename
    end
end

exit 0
