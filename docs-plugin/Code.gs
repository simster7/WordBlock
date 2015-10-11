/* What should the add-on do after it is installed */
function onInstall() {
  onOpen();
}
 
/* What should the add-on do when a document is opened */
function onOpen() {
  DocumentApp.getUi()
  .createAddonMenu() // Add a new option in the Google Docs Add-ons Menu
  .addItem("WordBlock", "showSidebar")
  .addToUi();  // Run the showSidebar function when someone clicks the menu
}
 
/* Show a 300px sidebar with the HTML from googlemaps.html */
function showSidebar() {
  var html = HtmlService.createTemplateFromFile("WordBlockSidebar")
    .evaluate()
    .setTitle("WordBlock"); // The title shows in the sidebar
  DocumentApp.getUi().showSidebar(html);
}