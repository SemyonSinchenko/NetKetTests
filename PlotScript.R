library(dplyr)
library(latex2exp)
library(ggplot2)
library(readr)
library(tidyr)

df <- read_csv("isingResultsFull.csv", col_names = F, na = c("None"), col_types = cols(.default = "d"))

colnames(df) <- c("prefix", "n_spins", "JZ", "h", "meanEnergy", "stdEnergy", "meanEnergyVariance", "stdEnergyVariance")

df_clean <- select(df, -prefix) %>%
    drop_na() %>%
    distinct() %>%
    mutate(y = -meanEnergy / (n_spins * JZ)) %>%
    mutate(x = h / JZ) %>%
    mutate(n_spins = as.factor(n_spins))

df_clean %>% head()

f <- ggplot(df_clean, aes(x = x, y = y, colour = n_spins)) +
    geom_point() +
    stat_smooth(method = "loess", se = F) +
    xlim(0, 12) +
    ylim(0, 12) +
    xlab(TeX("$\\frac{h}{J_z}$")) +
    ylab(TeX("$-\\frac{E}{N\\times J_z}$"))

print(f)

ggsave("plots/IsingOutputOfModelling.png", f, width = 12, height = 6)