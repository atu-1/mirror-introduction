ARGV.all? do |filename|
    if File.extname(filename) == '.py' then
        print filename
    end
end

exit 0
