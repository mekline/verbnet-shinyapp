library(shiny)
library(rPython)
library(rjson)
setwd("/Users/laurenskorb/Repos/shiny_verbnet/verbnet/")
python.load("/Users/laurenskorb/Repos/shiny_verbnet/verbnet/verbnet_search.py")

# Define server logic required to draw a histogram
function(input, output,session) {
   output$selectUI <- renderUI({ 
    selectInput("search2","Select your choice",python.call("first_choice",input$search1))
     
  })
}


