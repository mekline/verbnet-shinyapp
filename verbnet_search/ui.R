library(shiny)
library(rPython)
library(rjson)
library(RJSONIO)
library(shinythemes)
library(rsconnect)
library(methods)

#setwd("/Users/laurenskorb/Repos/shiny_verbnet/App-1/")
python.load("verbnet_search.py")
search_list<-c("verb","class","role","frame","")

# Define UI for application that draws a histogram

shinyUI(fluidPage(
  theme = shinytheme("united"),
  mainPanel(h2("Exploring Verbnet",align='center')),
  mainPanel(h5("Start by choosing either verb, class, thematic role, or syntactic frame 
               to search on. Then narrow your search according to your search category, 
               and receive a list of verbs that apply. Finally, choose a verb to see that 
               verb's class, syntactic frames, and thematic roles.")),
  mainPanel(selectInput('search1', label = "Search on:",choices = as.character(search_list),selected="")),
  mainPanel(
    div(style="display: inline-block",htmlOutput('selectUI')),
    div(style="display: inline-block;vertical-align:top; width: 50px;",HTML("<br>")),
    div(style="display: inline-block",downloadButton('downloadlist1', 'Download'))),
  mainPanel(br()),
  mainPanel(
    div(style="display: inline-block",htmlOutput('select2')),
    div(style="display: inline-block;vertical-align:top; width: 50px;",HTML("<br>")),
    div(style="display: inline-block",downloadButton('downloadlist2', 'Download'))),
  mainPanel(br()),
  mainPanel(htmlOutput("verb",container = pre))
  ))
