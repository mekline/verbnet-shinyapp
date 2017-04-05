library(shiny)
library(rPython)
library(rjson)
library(RJSONIO)
library(shinythemes)
library(rsconnect)
library(methods)

#setwd("/Users/laurenskorb/Repos/shiny_verbnet/App-1/")
python.load("verbnet_search.py")
search_list<-c("verb","class","role","frame")

# Define UI for application that draws a histogram

shinyUI(fluidPage(
  theme = shinytheme("united"),
  titlePanel("Exploring Verbnet"),
  mainPanel(selectInput('search1', label = h3("Search on:"),choices = as.character(search_list))),
  mainPanel(htmlOutput('selectUI')),
  mainPanel(downloadButton('downloadlist1', 'Download')),
  mainPanel(br()),
  mainPanel(htmlOutput('select2')),
  mainPanel(downloadButton('downloadlist2', 'Download')),
  mainPanel(br()),
  mainPanel(htmlOutput("verb",container = pre))
  ))
