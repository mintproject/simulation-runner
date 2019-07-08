library(ggplot2)
library(scales)

c <- data.frame(read.csv("/Users/rafsilva/Downloads/mint-penn-state-2/simulation-runner/cycles/output-summary.csv"))
d <- subset(c, year=='2017')

### Nitrogen Rate and Weed Fraction for a specific year
pdf(file="/Users/rafsilva/Downloads/cycles-nr-year-2017.pdf", height=5)
ggplot(d, aes(x=nitrogen_rate, y=yield, color=as.character(weed_fraction), linetype=as.character(weed_fraction))) + 
  geom_smooth() +
  xlab('Nitrogen Rate') +
  ylab('Grain Yield (Mg/ha)') +
  facet_wrap(~ location, ncol=4) +
  theme_light() +
  scale_color_hue('Weed Fraction') +
  scale_linetype_manual('Weed Fraction', values=c(2,3,4,5,6)) +
  theme(legend.position='bottom')
dev.off()

### Planting Dates and Weed Fraction
### Only analyzing fixed planting dates
d <- subset(d, planting_date_fixed=='True')
d <- subset(d, location=='8.88 North x 27.12 East')

ggplot(d, aes(x=planting_date, y=yield, color=as.character(weed_fraction))) + 
  geom_smooth() +
  xlab('Planting Day') +
  ylab('Grain Yield (Mg/ha)') +
  facet_wrap(~ nitrogen_rate, ncol=3) +
  scale_color_hue('Weed Fraction') +
  theme_light()



#### OLD PLOTS

pdf(file="/Users/rafsilva/Downloads/cycles-pd-year.pdf", height=5)
ggplot(d, aes(x=planting_date, y=yield)) + 
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
ggplot(d, aes(x=nitrogen_rate, y=yield)) + 
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

ggplot(d, aes(x=nitrogen_rate, y=yield)) + 
  geom_point(aes(shape=as.character(planting_date), color=as.character(planting_date))) + 
  geom_smooth(aes(color=location)) +
  xlab('Nitrogen Rate') +
  ylab('Grain Yield (Mg/ha)') +
  theme_light() +
  theme(legend.position = "bottom") + 
  scale_colour_hue() +
  scale_y_sqrt()
