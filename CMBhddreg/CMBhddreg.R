# clear variables and close windows
rm(list = ls(all = TRUE))
graphics.off()

# set working directory
setwd("")
options(stringsAsFactors = FALSE)

# install and load packages
libraries = c("sandwich", "lmtest", "lubridate")
lapply(libraries, function(x) if (!(x %in% installed.packages())) {
    install.packages(x)
})
lapply(libraries, library, quietly = TRUE, character.only = TRUE)

# read data
hdd.df = read.csv2("hdd.csv")

# date formatting (day sometimes missing)
datewday         = as.Date(hdd.df$date, "%Y %B %d")
day.na           = is.na(datewday)
datewday[day.na] = as.Date(paste(hdd.df$date[day.na], "1"), "%Y %B %d")
hdd.df$date      = datewday
day(hdd.df$date) = 1 # day not important for further analysis

# create month vector
months     = seq(min(hdd.df$date), max(hdd.df$date), "months")
months.int = seq(1, length(months))
month.df   = data.frame(date = months, int = months.int)

# merge dfs
hdd.df = merge(hdd.df, month.df, by = "date")

# regression
reg.lm  = lm(log(hdd.df$per.GB) ~ hdd.df$int)

# coefficients
print(coeftest(reg.lm, vcov. = vcovHC))

# R^2
paste("R^2:", summary(reg.lm)$r.squared)
