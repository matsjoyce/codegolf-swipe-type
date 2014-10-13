words = File.readlines('wordlist').map(&:chomp)

swipe = ARGV.shift
puts words.select {|word| word[0] == swipe[0] &&
                          word[-1] == swipe[-1]}
          .select {|word|
              chars = [word[0]]
              (1..word.size-1).each {|i| chars << word[i] if word[i] != word[i-1]}
              swipe[Regexp.new('^'+chars.join('.*')+'$')]
          }.sort_by {|word| word.size}[-1]