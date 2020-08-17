#install.packages("tidyverse")
#install.packages("rtweet")
#install.packages("tidytext")

#install.packages("SnowballC")
#install.packages("hunspell")

#install.packages("textdata")


library(tidyverse)
library(rtweet)
library(tidytext)

library(SnowballC)
library(hunspell)

library(textdata)

consumer_key <- '****'
consumer_key_secret <- '****'
appname <- '****'

access_token <- '****'
access_token_secret <- '****'

twitter_token <- create_token(app = appname,
                              consumer_key = consumer_key,
                              consumer_secret = consumer_key_secret,
                              access_token = access_token,
                              access_secret = access_token_secret)

trump_tweets <- search_tweets(q = "(from:realDonaldTrump)", include_rts = FALSE, n = 18000)
save_as_csv(trump_tweets, paste0("trump_", Sys.Date(), ".csv"))

aoc_tweets <- search_tweets(q = "(from:AOC)", include_rts = FALSE, n = 18000)
save_as_csv(aoc_tweets, paste0("aoc_", Sys.Date(), ".csv"))

mcconnell_tweets <- search_tweets(q = "(from:senatemajldr)", include_rts = FALSE, n = 18000)
save_as_csv(mcconnell_tweets, paste0("mcconnell_", Sys.Date(), ".csv"))

mccarthy_tweets <- search_tweets(q = "(from:GOPLeader)", include_rts = FALSE, n = 18000)
save_as_csv(mccarthy_tweets, paste0("mccarthy_", Sys.Date(), ".csv"))

schumer_tweets <- search_tweets(q = "(from:SenSchumer)", include_rts = FALSE, n = 18000)
save_as_csv(schumer_tweets, paste0("schumer_", Sys.Date(), ".csv"))

pelosi_tweets <- search_tweets(q = "(from:SpeakerPelosi)", include_rts = FALSE, n = 18000)
save_as_csv(pelosi_tweets, paste0("pelosi_", Sys.Date(), ".csv"))

bernie_tweets <- search_tweets(q = "(from:BernieSanders)", include_rts = FALSE, n = 18000)
save_as_csv(bernie_tweets, paste0("bernie_", Sys.Date(), ".csv"))

biden_tweets <- search_tweets(q = "(from:JoeBiden)", include_rts = FALSE, n = 18000)
save_as_csv(biden_tweets, paste0("biden_", Sys.Date(), ".csv"))

tlaib_tweets <- search_tweets(q = "(from:RashidaTlaib)", include_rts = FALSE, n = 18000)
save_as_csv(tlaib_tweets, paste0("tlaib_", Sys.Date(), ".csv"))

omar_tweets <- search_tweets(q = "(from:Ilhan)", include_rts = FALSE, n = 18000)
save_as_csv(omar_tweets, paste0("omar_", Sys.Date(), ".csv"))

ayanna_tweets <- search_tweets(q = "(from:AyannaPressley)", include_rts = FALSE, n = 18000)
save_as_csv(ayanna_tweets, paste0("ayanna_", Sys.Date(), ".csv"))
