library(ggplot2)
library(scales)

c <- data.frame(read.csv("/Users/rafsilva/Downloads/mint-penn-state-2/simulation-runner/cycles-output-summary.csv"))
c <- subset(c, year=='2017')

pdf(file="/Users/rafsilva/Downloads/cycles-pd-year.pdf", height=5)
ggplot(c, aes(x=planting_date, y=yield)) + 
  geom_point(aes(shape=as.character(nitrogen_rate), color=as.character(nitrogen_rate))) + 
  geom_smooth() +
  xlab('Planting Day') +
  ylab('Grain Yield (Mg/ha)') +
  facet_wrap(~ location, ncol=4) +
  theme_light() +
  theme(legend.position = "none") +
  scale_color_hue() +
  scale_y_sqrt()

dev.off()

pdf(file="/Users/rafsilva/Downloads/cycles-n-year.pdf", height=5)
ggplot(c, aes(x=nitrogen_rate, y=yield)) + 
  geom_point(aes(shape=as.character(planting_date), color=as.character(planting_date))) + 
  geom_smooth() +
  xlab('Nitrogen Rate') +
  ylab('Grain Yield (Mg/ha)') +
  facet_wrap(~ location, ncol=4) +
  theme_light() +
  theme(legend.position = "none") + 
  scale_color_hue() +
  scale_y_sqrt()
dev.off()

ggplot(c, aes(x=nitrogen_rate, y=yield)) + 
  geom_point(aes(shape=as.character(planting_date), color=as.character(planting_date))) + 
  geom_smooth(aes(color=location)) +
  xlab('Nitrogen Rate') +
  ylab('Grain Yield (Mg/ha)') +
  theme_light() +
  theme(legend.position = "bottom") + 
  scale_colour_hue() +
  scale_y_sqrt()
