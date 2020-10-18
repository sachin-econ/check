library(readstata13)
library(dplyr)
library(ggplot2)
data = read.dta13("sgn_2017.dta")
state = subset(data,
               STATEID == "Bihar 10" &
                 age >= 15 & age <= 65 & exper > 0 &
                 (indus_grp != 9 | indus_grp != 999))
Model_1 = lm(lnwrkwg ~ exper + expersq + eduyrs + sqeduyrs, data = state)
summary(Model_1)
state$mwrkwg = with(state, wrkwg / 12)
state$lnmwrkwg = with(state, log(mwrkwg + min(mwrkwg) + 1))
Model_2a = lm(lnmwrkwg ~ exper + expersq + eduyrs + sqeduyrs, data = state)
summary(Model_2a)
Model_2b = lm(lnwrkwg ~ age + sqage + eduyrs + sqeduyrs, state)
summary(Model_2b)
state$sqhage = with(state, sqage / 100)
Model_2c = lm(lnwrkwg ~ age + sqhage + eduyrs + sqeduyrs, state)
summary(Model_2c)
Model_3 = lm(lnwrkwg ~ exper + expersq + eduyrs + sqeduyrs + lnwrkhr, state)
summary(Model_3)
Model_5 = lm(lnwrkwg ~ exper + expersq + factor(educd) + lnwrkhr, state)
summary(Model_5)
statebx = state %>%
  select(c(ED3, hrlyearn, gender, lnhrwage)) %>%
  group_by(ED3, gender) %>%
  summarise(mean_wage = mean(hrlyearn)) %>%
  mutate(gender = as.factor(gender))
ggplot(data = statebx, aes(x = ED3, y = mean_wage, fill = gender)) +
  scale_fill_discrete(name = "Gender", labels = c("Male", "Female")) +
  labs(title = "Figure 1. Average (unadjusted) hourly wages by level of English", y =
         "Hourly Wages (Rs)", x = element_blank()) +
  geom_bar(position = 'dodge', stat = 'identity') +geom_text(aes(label = round(mean_wage, digits = 1)),
                                                             position = position_dodge(width = 0.9),
                                                             vjust = -0.25)
