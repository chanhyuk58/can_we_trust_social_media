library(tidyverse)
library(stargazer)
# library(rpart)

###### Accountlist #####
everypolitician <- read_csv("data/term-115.csv")
everypolitician <- everypolitician[,c("name", "twitter", "group", "area", "gender")]
names(everypolitician)[2] <- "user_screen_name"

accountlist <- read_csv("data/account_list_115.csv")
accountlist <- merge(accountlist, everypolitician, by = "user_screen_name", all.x = T)
write_csv(accountlist, file = "accountlist.csv", na = "")

accountlist2 <- read_csv("accountlist.csv")
voteview <- read_csv("../data/voteview/H115_members.csv")
voteview <- voteview[,c("icpsr", "party", "last_name", "state_abbrev", "born", "nominate_dim1")]

state.code <- read_csv("data/states.csv")
names(state.code) <- c("state", "state_abbrev")
voteview <- merge(voteview, state.code, by = "state_abbrev", all.x = T)

accountlist3 <- merge(accountlist2, voteview, by = c("state", "party", "last_name"), all.x = TRUE)
write_csv(accountlist3, file = "accountlist2.csv", na = "")

##### Bills Subjects #####
bills115 <- read_csv("../data/bills.csv")
billslist115 <- read_csv("../data/tweet_by_bills.csv")
billslist115 <- billslist115[billslist115$size > 0, ]
bills115 <- merge(billslist115, bills115, by = "bill_number", all.x = T)
bills115 <- bills115[, c("bill_number", "title", "sponsor", "top_term", 
                         "congress", "clerk_rollnumber")
]
bills116 <- read_csv("~/Data/twitter_congress/116th/data/bills.csv")
billslist116 <- read_csv("~/Data/twitter_congress/116th/data/tweet_by_bills.csv")
billslist116 <- billslist116[billslist116$size > 0, ]
bills116 <- merge(billslist116, bills116, by = "bill_number", all.x = T)
bills116 <- bills116[, c("bill_number", "title", "sponsor", "top_term", 
                         "congress", "clerk_rollnumber")
]
bills <- rbind(bills115, bills116)
write.csv(bills, file = "data/bills_subjects.csv", row.names = FALSE)


##### final data ######
voteview2 <- read_csv("~/Data/twitter_congress/116th/data/voteview/H116_members.csv")
df115 = read_csv("../data/final.csv")
df115 <- merge(df115, bills[c(1,4,5)], by = c('bill_number', 'congress'), all.x = TRUE)
df115 <- merge(df115, voteview[,c("nominate_dim1", "icpsr")], by = "icpsr", all.x = TRUE)
df116 = read_csv("~/Data/twitter_congress/116th/data/final.csv")
df116 <- merge(df116, bills[c(1,4,5)], by = c('bill_number', 'congress'), all.x = TRUE)
df116 <- merge(df116, voteview2[,c("nominate_dim1", "icpsr")], by = "icpsr", all.x = TRUE)
df = rbind(df115, df116)
df$party2 = ifelse(df$party == "D", "Democrat", "Republican")
df$yea2 <- ifelse(df$yea_1 == 1, "Yea", "Nay")
df$yea3 <- ifelse(df$yea_1 == 1, 1, 0)
df$positive <- ifelse(df$score1 > 0, 1, 
                      ifelse(df$score1 < 0 , -1, 0))
df1 = df[df$tweet_id > 2,]



##### Graph #####
# tree <- rpart(yea_1 ~ score1, data = df)
# plot_tree <- function(tree, x, y) {
#   s <- seq(-1, 1, by=.01)
#   plot(x, y)
#   lines(s, predict(tree, data.frame(x=s)))
# }
# plot_tree(tree, df$score1, df$yea_1)
p1 <- ggplot(data = na.omit(df1[,]), aes(x = yea2, y = score1)) +
  geom_boxplot() +
  facet_wrap(~ party2) + 
  xlab("Roll Call Records") +
  ylab("Tweet Sentiment Score") +
  theme(text = element_text(size = 20))
p1
ggsave(p1, filename = "figures/boxplot_all.pdf")

p2 <- ggplot(data = df1[df1$congress == 115, ], aes(x = score1, y = yea3)) +
  # facet_wrap(~top_term) +
  geom_smooth(method = "glm", method.args = list(family = "binomial"),
              aes(x = score1, y = yea3), se = FALSE, 
              color = "grey60", alpha = 0.5) +
  geom_jitter(width = .1, height = .08, aes(color = party, shape = party), alpha = 0.5) +
  scale_color_manual(values = c("blue", "red")) +
  xlab("Sentiment Score") +
  ylab("Roll Call Vote Records") +
  scale_y_continuous(breaks = c(1,0), labels=c("1" = "Yea", "0" = "Nay")) +
  guides(color=guide_legend(title="Party")) +
  theme(text = element_text(size = 20),
        legend.position = "None",
        legend.title = element_text(size = 15),
        legend.text = element_text(size = 12))
p2
ggsave(p2, filename = "figures/p2_115.pdf", width = 5, height = 5)

p3 <- ggplot(data = df1[ !is.na(df1$top_term), ], aes(x = score1, y = yea3)) +
  facet_wrap(~top_term) +
  geom_jitter(width = .1, height = .08, aes(color = party), alpha = 0.5) +
  scale_color_manual(values = c("blue", "red")) +
  xlab("Sentiment Score") +
  ylab("Roll Call Vote Records") +
  scale_y_continuous(breaks = c(1,0), labels=c("1" = "Yea", "0" = "Nay")) +
  guides(color=guide_legend(title="Party")) +
  theme(text = element_text(size = 10),
        legend.title = element_text(size = 10),
        legend.text = element_text(size = 8))
p3
ggsave(p3, filename = "figures/p1_top_term.pdf", width = 15, height = 10)

bar <- ggplot(data = df1[df1$congress == 116, ]) +
  geom_bar(aes(x = positive, fill = party), stat = "count") +
  scale_fill_manual(values = c("blue", "red")) +
  xlab("sentiment") +
  ylab("number of obs") +
  guides(fill=guide_legend(title="Party")) +
  theme(text = element_text(size = 20),
        legend.title = element_text(size = 14),
        legend.text = element_text(size = 12))
bar
ggsave(bar, filename = "figures/bar116.pdf", width = 7, height = 7)



#### Regression ####
lm1 <- df%>% 
  mutate(commit = tweet_id*days, 
         extreme = abs(nominate_dim1)) %>% 
  lm(-commit ~ gender + sponsor3 + born 
     # + factor(party)
     # + factor(congress)
     , data = .)
summary(lm1)
stargazer(lm1)
