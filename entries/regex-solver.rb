words = File.readlines('wordlist').map(&:chomp)

swipe = ARGV.shift
puts words.select {|word| word[0] == swipe[0] &&
                          word[-1] == swipe[-1] &&
                          swipe[Regexp.new('^'+word.chars.join('.*')+'$')] }
          .sort_by {|word| word.size}[-1]