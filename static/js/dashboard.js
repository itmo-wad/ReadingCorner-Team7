function loadResult(bookIsbn, title) {
  const s = JSON.stringify({ bookIsbn, title });
  $.ajax({
    url: "/add-book",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify(s)
  });
}

function readBook(bookIsbn) {
  localStorage.setItem("isbn", bookIsbn);
}

function search(ele) {
  if (event.key === 'Enter') {
    document.getElementById("search").click();
  }
}

$(document).ready(function () {
  var item, tile, author, publisher, bookLink, bookImg;
  var outputList = document.getElementById("search-output");
  var bookUrl = "https://www.googleapis.com/books/v1/volumes?q=";
  var apiKey = "key=AIzaSyDtXC7kb6a7xKJdm_Le6_BYoY5biz6s8Lw";
  var placeHldr = "https://via.placeholder.com/150";
  var searchData;
  var typeResearch;
  var name;

  // Listener for quit-search button
  $("#quit-search").click(function () {
    document.getElementById("quit-search").hidden = true;
    document.getElementById("bookshelf").hidden = false;
    $("#search-box").val("");
    document.getElementById("selection-mode").value = "title";
    outputList.innerHTML = "";
  });

  //listener for search button
  $("#search").click(function () {
    outputList.innerHTML = "";
    document.body.style.backgroundImage = "url('')";
     searchData = $("#search-box").val(); // Prend la valeur rentrée par l'user dans la barre de recherche
     typeResearch = $("#selection-mode").val();
     //handling empty search input field
     if(searchData !== "" && searchData !== null) {
      if (typeResearch==='title'){
        name = bookUrl + searchData + " &filter=partial" ;//+ " &filter=partial"
      }
      if (typeResearch==='author'){
        name = bookUrl + " '' +inauthor:"+searchData;
      }
      if (typeResearch==='subject'){
        name = bookUrl +" '' +subject:"+searchData;
      }
      document.getElementById("quit-search").hidden = false;
      document.getElementById("bookshelf").hidden = true;
       // $.get("https://www.googleapis.com/books/v1/volumes?q="+searchData, getBookData()});
       $.ajax({
          url : name ,
          dataType: "json",
          success: function(response) {
            if (response.totalItems === 0) {
              alert("no result!.. try again")
            }
            else {
              $("#title").animate({'margin-top': '5px'}, 1000); //search box animation
              $(".book-list").css("visibility", "visible");
              displayResults(response); // Appelle la fonction qui afffiche les résultats
              //loadResult(response);
            }
          },
          error: function () {
            alert("Something went wrong.. <br>"+"Try again!");
          }
        });
      }
      $("#search-box").val(""); //clearn search box
   });



   function displayResults(response) {
      for (var i = 0; i < response.items.length; i+=2) {
        item = response.items[i];
        title1 = item.volumeInfo.title;
        author1 = item.volumeInfo.authors;
        publisher1 = item.volumeInfo.publisher;
        bookLink1 = item.volumeInfo.previewLink;
        bookIsbn = item.volumeInfo.industryIdentifiers[1].identifier
        bookImg1 = (item.volumeInfo.imageLinks) ? item.volumeInfo.imageLinks.thumbnail : placeHldr ;
        viewability = item.accessInfo.viewability;
        
        item2 = response.items[i+1];
        title2 = item2.volumeInfo.title;
        author2 = item2.volumeInfo.authors;
        publisher2 = item2.volumeInfo.publisher;
        bookLink2 = item2.volumeInfo.previewLink;
        bookIsbn2 = item2.volumeInfo.industryIdentifiers[1].identifier
        bookImg2 = (item2.volumeInfo.imageLinks) ? item2.volumeInfo.imageLinks.thumbnail : placeHldr ;
        viewability2 = item2.accessInfo.viewability;
        //loadResult(bookLink1);
        // in production code, item.text should have the HTML entities escaped.
        outputList.innerHTML += '<div class="row mt-4">' +
                                formatOutput(bookImg1, title1, author1, publisher1, bookLink1, bookIsbn, viewability) +
                                formatOutput(bookImg2, title2, author2, publisher2, bookLink2, bookIsbn2, viewability2) +                                
                                '</div>';
      }
   }

   /*
   * card element formatter using es6 backticks and templates (indivial card)
   * @param bookImg title author publisher bookLink
   * @return htmlCard
   */
   function formatOutput(bookImg, title, author, publisher, bookLink, bookIsbn, viewability) {
     //var viewUrl = 'book.html?isbn='+bookIsbn; //constructing link for bookviewer
     var js_title = title.split('\'').join('\\\'');
     var viewUrl = 'https://www.googleapis.com/books/v1/volumes?q=""+book.html?isbn:'+bookIsbn; //constructing link for bookviewer
     var lien = `<a> </a>`;
     if (viewability !== "NO_PAGES") {
      lien = `<a target="_blank" href=/viewer class="btn btn-secondary" onclick = "readBook(${bookIsbn})">Read Book </a>` ;
    }
     var htmlCard = `<div class="col-lg-6">
       <div class="card" style="">
         <div class="row no-gutters">
           <div class="col-md-4">
             <img src="${bookImg}" class="card-img" alt="...">
           </div>
           <div class="col-md-8">
             <div class="card-body">
               <h5 class="card-title">${title}</h5>
               <p class="card-text">Author: ${author}</p>
               <p class="card-text">Publisher: ${publisher}</p>
               ${lien}
               <a href=javascript:void(0); onclick = "loadResult(${bookIsbn}, '${js_title}')"> Add to my lectures </a>
             </div>
           </div>
         </div>
       </div>
     </div>`
    return htmlCard;
  }
  //<a target="_blank" href=/viewer class="btn btn-secondary" data-isbn='${bookIsbn}'>Read Book </a>
  // <a target="_blank" href=javascript:void(0); class="btn btn-secondary" onclick = "readBook(${bookIsbn})">Read Book </a>
  //<a href=javascript:void(0); onclick = "loadResult(${bookIsbn}, '${js_title}')"> Add to my lectures </a>
});
