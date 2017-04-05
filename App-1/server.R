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
   output$select2 <- renderUI({
     selectInput("search3","Select your verb",python.call("second_choice",input$search1,input$search2))
   })
   output$verb <- renderUI({
    python.call("final_print",input$search3) })
}


