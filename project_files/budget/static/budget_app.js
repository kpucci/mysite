/**
* Sets up basic things needed for the page to work properly
*/
function setup(){
    // Populate year dropdown list with the past 5 years + the current year
    var currYear = (new Date()).getFullYear();
    var yearIndexList = [-5,-4,-3,-2,-1,0];
    yearIndexList.map(createYearDropdown(currYear));
    var dateInput = document.getElementById("purchase-date")
    dateInput.min = (currYear-5)+"-01-01";
    dateInput.max = currYear+"-12-31";

    // If month and year selection previously stored in session, set date to those values
    if(sessionStorage.getItem("month") != null && sessionStorage.getItem("year") != null){
        document.getElementById("month-dropdown").value = sessionStorage.getItem("month");
        document.getElementById("year-dropdown").value = sessionStorage.getItem("year");
    }else{
        // Otherwise, save the original values in localStorage
        storeDateSelection();
    }


    // Assign event listeners
    document.getElementById("add-purchase-button").addEventListener("click", addPurchase, true);
    document.getElementById("add-cat-button").addEventListener("click", addCategory, true);
    document.getElementById("month-dropdown").addEventListener("change",storeDateSelection);
    document.getElementById("year-dropdown").addEventListener("change",storeDateSelection);

    // Get the list of categories and populate summaries in main view
    getCats();
}

/**
* Creates a dropdown list to select a year
* @param {Number} currYear
* @param {Array item} item
* @return {Function} addToYearDropdown
*/
function createYearDropdown(currYear){
    function addToYearDropdown(item){
        var yearDropdown = document.getElementById("year-dropdown");
        var option = document.createElement("option");
        option.text = currYear + item;
        yearDropdown.add(option);
    }
    return addToYearDropdown;
}

/**
* Save current date selection in session storage
*/
function storeDateSelection(){
    // Store current date selection in storage so it doesn't reset every time the page is reloaded
    var month_sel = document.getElementById("month-dropdown").value;
    var year_sel = document.getElementById("year-dropdown").value;
    // NOTE: Use session storage so you can open another page and get summaries for a different date
    sessionStorage.setItem("month", month_sel);
    sessionStorage.setItem("year", year_sel);
    getCats();
}

/**
* Makes an HTTP request
* @param {Function} method - HTTP method (GET, POST, etc.)
* @param {String} target - Resource URL
* @param {Number} retCode - Expected return code
* @param {Function} callback - Callback method to execute once request has completed
* @param {String} data - Data to send with request
*/
function makeReq(method, target, retCode, callback, data){
    // Create new request
    var httpRequest = new XMLHttpRequest();

	if (!httpRequest){
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

    // On state change of request, makeHandler
	httpRequest.onreadystatechange = makeHandler(httpRequest, retCode, callback);

    // Open the request
	httpRequest.open(method, target);

    // If the request contains data
	if (data){
		httpRequest.setRequestHeader('Content-Type', 'application/json');
		httpRequest.send(data);
	}else{
		httpRequest.send();
	}
}

/**
* Function to handle the reqeust
* @param {XMLHttpRequest} httpRequest
* @param {Number} retCode - Expected return code
* @param {Function} callback - Callback method
*/
function makeHandler(httpRequest, retCode, callback){
	function handler() {
        // If request has been completed
		if (httpRequest.readyState === XMLHttpRequest.DONE){
            // If return code is as expected
            if (httpRequest.status === retCode){
				console.log("received response text:  " + httpRequest.responseText);
				callback(httpRequest.responseText);     // Call callback method on response text
			}else if(httpRequest.status == 0){
				console.log("received response text:  " + httpRequest.responseText);
				callback(httpRequest.responseText);
			}else{
				alert("There was a problem with the request.  You'll need to refresh the page!");
				alert(httpRequest.status);
			}
		}
	}
	return handler;
}

/**
* Get category list
*/
function getCats() {
    // console.log("Get Categories");
	makeReq("GET", "/budget/cats", 200, showCategories);
}

/**
* Add a purchase to purchase list
*/
function addPurchase(){
    var purchaseName = document.getElementById("purchase-name-input").value;    // Get the purchase name from input
    var purchaseAmount = document.getElementById("purchase-amount-input").value;    // Get the purchase amount from input
    var purchaseDate = document.getElementById("purchase-date").value;  // Get purchase date from input
    var purchaseDateSplit = purchaseDate.split("-");    // Split the date at "-" (format is year-month-day)
    var year = purchaseDateSplit[0];    // Get the year
    var month = purchaseDateSplit[1];   // Get the month
    var day = purchaseDateSplit[2];     // Get the day

    var cat_dropdown = document.getElementById("cat-dropdown");     // Get the category list dropdown

    // If the user inputs are okay, make AJAX request
    if(verifyInputs(purchaseName,purchaseAmount,"purchase")){
        var purchaseAmountNum;
        // If the user put a $ before the number, remove it
        if(purchaseAmount.startsWith("$")){
            purchaseAmountNum = purchaseAmount.slice(1);
        }else{
            purchaseAmountNum = purchaseAmount;
        }
        var category = cat_dropdown.options[cat_dropdown.selectedIndex].text;   // Get the selected category

        // Create the data for the request
        var data;
    	data = '{"name":"' + purchaseName + '","amount":' + purchaseAmountNum + ',"category":"' + category + '","date":"' + purchaseDate +'"}';

        // Make AJAX request to post new purchase to purchase list
        makeReq("POST", "/budget/purchases", 201, getCats, data);

        // Clear input boxes
    	document.getElementById("purchase-name-input").value = "";
        document.getElementById("purchase-amount-input").value = "";
    }
}

/**
* Add a category to category list
*/
function addCategory(){
    var categoryName = document.getElementById("cat-name-input").value;     // Get category name from input
    var categoryBudget = document.getElementById("cat-budget-input").value; // Get budget from input

    // If user inputs are okay, make AJAX request
    if(verifyInputs(categoryName,categoryBudget,"category")){
        // Create data for request
        var data;
        data = '{"name":"' + categoryName + '","budget":' + categoryBudget + '}';

        // Make AJAX request to post new category to category list
        makeReq("POST", "/budget/cats", 201, getCats, data);

        // Clear input boxes
        document.getElementById("cat-name-input").value = "";
        document.getElementById("cat-budget-input").value = "";
    }
}

/**
* Verify the inputs from user
* @param {String} name - name
* @param {String} amount - amount
* @param {String} type - purchase or category
* @return {Bool} - true if inputs are okay, false if there was an error
*/
function verifyInputs(name,amount,type){
    var amountRegex = /^\$?(?=\d|\.)\d*\.?\d{0,2}$/; // Regex to validate format of amount

    // If name is empty, warn user and return false
    if(name == ""){
        alert("Please provide a name for your " + type);
        return false;
    }
    // If amount is empty, warn user and return false
    if(amount == ""){
        alert("Please provide an amount for your " + type);
        return false;
    }
    // If amount has wrong syntax, warn user and return false
    if(!amountRegex.test(amount)){
        alert("Invalid syntax for " + type + " amount");
        return false;
    }
    // Otherwise, return true
    return true;
}

/**
* Get attribute of object in list
* @param {String} attrName - name of attribute
* @param {Array item} item - object in list that's being mapped
* @return {String} item attribute
* @return {Function} attrGetter
*/
function getAttr(attrName){
    function attrGetter(item){
        return item[attrName];
    }
    return attrGetter;
}

/**
* Populate category summary view
* @param {String} responseText - response text from AJAX request
*/
function showCategories(responseText){
    console.log("Repopulating category summaries...");

    // Get category list from response
    var categories = JSON.parse(responseText);

    // Remove old category summaries
    var categories_container = document.getElementById("categories-container");
    while(categories_container.hasChildNodes()){
        categories_container.removeChild(categories_container.childNodes[0]);
    }

    // Remove old category dropdown list
    var cat_dropdown = document.getElementById("cat-dropdown");
    while(cat_dropdown.hasChildNodes()){
        cat_dropdown.removeChild(cat_dropdown.childNodes[0]);
    }

    // Get list of category names and repopulate category dropdown list
    var cat_names = categories.map(getAttr('name'));
    cat_names.map(addCatToDropdown);

    // Get list of category budgets
    var cat_budgets = categories.map(getAttr('budget'));

    // Get list of category purchase lists
    var cat_purchases = categories.map(getAttr('purchases'));

    // For each purchase list, get percent spent of purchases
    // var percent_spent = cat_purchases.map(getPercentSpent(cat_budgets));
    var purch_totals = cat_purchases.map(getPurchaseTotals);

    // Create array of colors to use for summaries
    var colors = ["#ff913b","#ffe83a","#b0ff39","#38ff3c","#37ffb6",
                  "#36fffb","#35a1ff","#3438ff","#9233ff","#ff32fb",
                  "#ff31a6","#ff3067"];

    // Create summaries
    // percent_spent.map(createSummaries(cat_names,colors));
    purch_totals.map(createSummaries(cat_names,cat_budgets,colors));

    // Create clear div to clear float property
    createClear("categories-container");

    // Get total of all purchases
    var all_purch_total = purch_totals.reduce(add,0);

    // Create summary of uncategorized purchases
    createUncategorizedSummary(purch_totals[purch_totals.length-1],all_purch_total);

    // Create clear div to clear float property
    createClear("uncat-container");
    console.log("Repopulating done.");
}

/**
* Filter purchases by month and year
* @param {String} month
* @param {String} year
* @param {Object} purch - purchase object
* @return {Array} list of filtered purchases
* @return {Function} filterPurchases function
*/
function filterByDate(month,year){
    function filterPurchases(purch){
        var purchDate = purch["date"].split("-");   // Get purchase date
        var purchYear = parseInt(purchDate[0]);   // Get purchase year
        var purchMonth = parseInt(purchDate[1]);  // Get purchase month
        return (purchYear == parseInt(year) && purchMonth == parseInt(month));
    }
    return filterPurchases;
}

/**
* Add two numbers together
* @param {Number} a
* @param {Number} b
* @return {Number} sum
*/
function add(a,b){
    return a+b;
}

/**
* Helper function to get purchase totals
* @param {Array} purchList - List of purchases
* @param {Number} index - Current index
*/
function getPurchaseTotals(purchList,index){
    // Get month and year from dropdown lists
    var selMonth = document.getElementById("month-dropdown").value;
    var selYear = document.getElementById("year-dropdown").value;

    // Get list of purchases that match the month and year
    var filter_purch = purchList.filter(filterByDate(selMonth,selYear));

    // Get list of purchase amounts from filtered list
    var purch_amounts = filter_purch.map(getAttr('amount'));
    return purch_amounts.reduce(add,0);
}

/**
* Calculate percentage of budget spent
* @param {Number} total - total sum of purchases for category
* @param {Number} budget - allowed budget for category
* @return {Number} percentage of budget spent
*/
function percentSpent(total,budget){
    return ((total/budget)*100).toFixed(1);
}

/**
* Helper function for percentSpent
* @param {Number} budget - allowed budget for category
* @param {Array} purchList - list of purchases
* @param {Number} index - current index
* @return {Array} list of percent spent for categories
* @return {Function} subPercentSpent helper
*/
function getPercentSpent(budget){
    function subPercentSpent(purchList, index){
        // Get month and year from dropdown lists
        var selMonth = document.getElementById("month-dropdown").value;
        var selYear = document.getElementById("year-dropdown").value;

        // Get list of purchases that match the month and year
        var filter_purch = purchList.filter(filterByDate(selMonth,selYear));

        // Get list of purchase amounts from filtered list
        var purch_amounts = filter_purch.map(getAttr('amount'));
        return percentSpent(purch_amounts.reduce(add,0),budget[index]);
    }
    return subPercentSpent;
}

/**
* Add category to dropdown list for purchase creation
* @param {String} catName - name of category
*/
function addCatToDropdown(catName){
    var dropdown = document.getElementById("cat-dropdown");
    var option = document.createElement("option");
    option.text = catName;
    dropdown.add(option);
}

/**
* Helper function for createSummary
* @param {Array} nameArr - list of category names
* @param {Array} budgetArr - list of category budgets
* @param {Array} colorArr - list of color hex codes
* @return {Function} summaryCreation helper
*/
function createSummaries(nameArr,budgetArr,colorArr){
    function summaryCreation(total,index){
        // if(spent != "NaN" && spent != "Infinity"){
            // createSummary(nameArr[index],budgetArr[index],spent,colorArr[index]);
        createSummary(nameArr[index],budgetArr[index],total,colorArr[index]);
        // }
    }
    return summaryCreation;
}

/**
* Create a summary of each category
* @param {String} catName - category name
* @param {Number} budget - category budget
* @param {Number} spent - percet spent of budget
* @param {String} color - hex code of color for summary
*/
function createSummary(catName,budget,total,color){
    // Get percent spent of budget
    var spent = percentSpent(total,budget);
    var spent_nearest5;
    // If percent spent is over 100%, mark with 105 flag
    if(spent == "NaN" || spent == "Infinity"){
        return;
    }else if(spent>100){
        spent_nearest5 = 105;
    }else{
        // Otherwise, calculate the percent to the nearest 5%
        spent_nearest5 = (Math.round(spent/5.0))*5;
    }

    // Get categories container
    var categories_container = document.getElementById("categories-container");

    // Create new container for category
    var category_container = document.createElement("div");
    category_container.className = "category-container";

    // Create new container for category name
    var cat_name_container = document.createElement("div");
    cat_name_container.className = "cat-name-container";

    // Create new heading for category name and append to container
    var cat_name = document.createElement("h2");
    cat_name.className = "cat-name";
    cat_name.innerHTML = catName;
    cat_name.style.color = color;
    cat_name_container.appendChild(cat_name);

    // Create new container for summary chart
    var summary_container = document.createElement("div");
    summary_container.className = "summary-container";

    // Create containers for each quadrant of chart
    var slice_up_right = document.createElement("div");
    var slice_down_right = document.createElement("div");
    var slice_down_left = document.createElement("div");
    var slice_up_left = document.createElement("div");

    // Set color of summary chart
    slice_up_right.style.backgroundColor = color;
    slice_down_right.style.backgroundColor = color;
    slice_down_left.style.backgroundColor = color;
    slice_up_left.style.backgroundColor = color;

    // Set animation for summary
    setAnimationClasses(slice_up_right,slice_down_right,slice_down_left,slice_up_left,spent_nearest5);

    // Append quadrants to summary container
    summary_container.appendChild(slice_up_right);
    summary_container.appendChild(slice_down_right);
    summary_container.appendChild(slice_down_left);
    summary_container.appendChild(slice_up_left);

    // Create container for percent
    var percent_container = document.createElement("div");
    percent_container.className = "percent-container";

    // Create container for percent spent text and appent to percent container
    var number_container = document.createElement("div");
    number_container.className = "number-container";
    number_container.innerHTML = spent + '%';
    percent_container.appendChild(number_container)

    // Append percent container to summary container
    summary_container.appendChild(percent_container);

    // Create container for budget
    var budget_container = document.createElement("div");
    budget_container.className = "budget-container";
    budget_container.innerHTML = "$" + total + " / $" + budget;

    // Create container for edit button
    var edit_button_container = document.createElement("div");
    edit_button_container.className = "edit-button-container";

    // Create edit button and append to edit button container
    var edit_button = document.createElement("button");
    var catNameDash = catName.trim().replace(/ /g,"-");
    edit_button.value = catNameDash;
  	edit_button.innerHTML = "Edit";
  	edit_button.id = "edit-"+catNameDash;
    edit_button.name = "edit-button";
    edit_button.className = "edit-button";
    edit_button.type = "button";
    edit_button.addEventListener("click", function(){openModal(catName,budget)}, true);
    edit_button_container.appendChild(edit_button);

    // Append category name, summary, budget, and edit button containers to category container
    category_container.appendChild(cat_name_container);
    category_container.appendChild(summary_container);
    category_container.appendChild(budget_container);
    category_container.appendChild(edit_button_container);

    // Append category container to categories container
    categories_container.appendChild(category_container);
}

/**
* Set animation classes for four slices of summary chart
* @param {div} upRight - Upper right quadrant div
* @param {div} downRight - Lower right quadrant div
* @param {div} downLeft - Lower left quadrant div
* @param {div} upLeft - Upper left quadrant div
* @param {Number} switchNum - Percent spent rounded to nearest 5%
*/
function setAnimationClasses(upRight,downRight,downLeft,upLeft,switchNum){
    switch(switchNum){
        case 0:
            upRight.className = "slice-up-right right-up-0";
            downRight.className = "slice-down-right";
            downLeft.className = "slice-down-left";
            upLeft.className = "slice-up-left";
            break;
        case 5:
            upRight.className = "slice-up-right right-up-5";
            downRight.className = "slice-down-right";
            downLeft.className = "slice-down-left";
            upLeft.className = "slice-up-left";
            break;
        case 10:
            upRight.className = "slice-up-right right-up-10";
            downRight.className = "slice-down-right";
            downLeft.className = "slice-down-left";
            upLeft.className = "slice-up-left";
            break;
        case 15:
            upRight.className = "slice-up-right right-up-15";
            downRight.className = "slice-down-right";
            downLeft.className = "slice-down-left";
            upLeft.className = "slice-up-left";
            break;
        case 20:
            upRight.className = "slice-up-right right-up-20";
            downRight.className = "slice-down-right";
            downLeft.className = "slice-down-left";
            upLeft.className = "slice-up-left";
            break;
        case 25:
            upRight.className = "slice-up-right right-up-25";
            downRight.className = "slice-down-right";
            downLeft.className = "slice-down-left";
            upLeft.className = "slice-up-left";
            break;
        case 30:
            upRight.className = "slice-up-right right-up-25";
            downRight.className = "slice-down-right right-down-30";
            downLeft.className = "slice-down-left";
            upLeft.className = "slice-up-left";
            break;
        case 35:
            upRight.className = "slice-up-right right-up-25";
            downRight.className = "slice-down-right right-down-35";
            downLeft.className = "slice-down-left";
            upLeft.className = "slice-up-left";
            break;
        case 40:
            upRight.className = "slice-up-right right-up-25";
            downRight.className = "slice-down-right right-down-40";
            downLeft.className = "slice-down-left";
            upLeft.className = "slice-up-left";
            break;
        case 45:
            upRight.className = "slice-up-right right-up-25";
            downRight.className = "slice-down-right right-down-45";
            downLeft.className = "slice-down-left";
            upLeft.className = "slice-up-left";
            break;
        case 50:
            upRight.className = "slice-up-right right-up-25";
            downRight.className = "slice-down-right right-down-50";
            downLeft.className = "slice-down-left";
            upLeft.className = "slice-up-left";
            break;
        case 55:
            upRight.className = "slice-up-right right-up-25";
            downRight.className = "slice-down-right right-down-50";
            downLeft.className = "slice-down-left left-down-55";
            upLeft.className = "slice-up-left";
            break;
        case 60:
            upRight.className = "slice-up-right right-up-25";
            downRight.className = "slice-down-right right-down-50";
            downLeft.className = "slice-down-left left-down-60";
            upLeft.className = "slice-up-left";
            break;
        case 65:
            upRight.className = "slice-up-right right-up-25";
            downRight.className = "slice-down-right right-down-50";
            downLeft.className = "slice-down-left left-down-65";
            upLeft.className = "slice-up-left";
            break;
        case 70:
            upRight.className = "slice-up-right right-up-25";
            downRight.className = "slice-down-right right-down-50";
            downLeft.className = "slice-down-left left-down-70";
            upLeft.className = "slice-up-left";
            break;
        case 75:
            upRight.className = "slice-up-right right-up-25";
            downRight.className = "slice-down-right right-down-50";
            downLeft.className = "slice-down-left left-down-75";
            upLeft.className = "slice-up-left";
            break;
        case 80:
            upRight.className = "slice-up-right right-up-25";
            downRight.className = "slice-down-right right-down-50";
            downLeft.className = "slice-down-left left-down-75";
            upLeft.className = "slice-up-left left-up-80";
            break;
        case 85:
            upRight.className = "slice-up-right right-up-25";
            downRight.className = "slice-down-right right-down-50";
            downLeft.className = "slice-down-left left-down-75";
            upLeft.className = "slice-up-left left-up-85";
            break;
        case 90:
            upRight.className = "slice-up-right right-up-25";
            downRight.className = "slice-down-right right-down-50";
            downLeft.className = "slice-down-left left-down-75";
            upLeft.className = "slice-up-left left-up-90";
            break;
        case 95:
            upRight.className = "slice-up-right right-up-25";
            downRight.className = "slice-down-right right-down-50";
            downLeft.className = "slice-down-left left-down-75";
            upLeft.className = "slice-up-left left-up-95";
            break;
        case 100:
            upRight.className = "slice-up-right right-up-25";
            downRight.className = "slice-down-right right-down-50";
            downLeft.className = "slice-down-left left-down-75";
            upLeft.className = "slice-up-left left-up-100";
            break;
        case 105:
            upRight.className = "slice-up-right right-up-25";
            downRight.className = "slice-down-right right-down-50";
            downLeft.className = "slice-down-left left-down-75";
            upLeft.className = "slice-up-left left-up-100";
            upRight.style.backgroundColor = "#ff3030";
            downRight.style.backgroundColor = "#ff3030";
            downLeft.style.backgroundColor = "#ff3030";
            upLeft.style.backgroundColor = "#ff3030";
            break;
    }
}

/**
* Create summary for uncategorized purchases
* @param {Number} uncatTotal - Total of uncategorized purchases
* @param {Number} purchTotal - Total of all purchases
*/
function createUncategorizedSummary(uncatTotal,purchTotal){
    // Get percentage of uncategorized purchases to total purchases
    var uncat_percent = percentSpent(uncatTotal,purchTotal);
    var uncat_percent_5;
    // If percent spent is over 100%, mark with 105 flag
    if(uncat_percent == "NaN" || uncat_percent == "Infinity"){
        return;
    }else if(uncat_percent>100){
        uncat_percent_5 = 105;
    }else{
        // Otherwise, calculate the percent to the nearest 5%
        uncat_percent_5 = (Math.round(uncat_percent/5.0))*5;
    }

    // Create containers for each quadrant of chart
    var slice_up_right = document.getElementById("uncat-up-right");
    var slice_down_right = document.getElementById("uncat-down-right");
    var slice_down_left = document.getElementById("uncat-down-left");
    var slice_up_left = document.getElementById("uncat-up-left");

    // Set color of summary chart
    slice_up_right.style.backgroundColor = "white";
    slice_down_right.style.backgroundColor = "white";
    slice_down_left.style.backgroundColor = "white";
    slice_up_left.style.backgroundColor = "white";

    // Setup animation for summary
    setAnimationClasses(slice_up_right,slice_down_right,slice_down_left,slice_up_left,uncat_percent_5);

    var number_container = document.getElementById("uncat-number");
    number_container.innerHTML = uncat_percent + '%';

    var uncat_total = document.getElementById("uncat-total");
    uncat_total.innerHTML = "Total: $" + uncatTotal;
}

/**
* Create div with clear:both to fix float issues
* @param {String} parentName - name of parent element to add clear div
*/
function createClear(parentName){
    var parent_container = document.getElementById(parentName);
    var clear_container = document.createElement("div");
    clear_container.className = "clear";
    parent_container.appendChild(clear_container);
}

/**
* Open modal for editing category
* @param {String} name - Category name
* @param {Number} budget - Category budget
*/
function openModal(name,budget){
    document.getElementById("edit-cat-header").innerHTML = "Edit " + name;
    document.getElementById("edit-cat-header").value = name;
    document.getElementById("edit-budget-input").value = budget;
    document.getElementById("edit-cat-modal").style.display="block";

    document.getElementById("save-button").addEventListener("click", saveCat);
    document.getElementById("delete-button").addEventListener("click", deleteCat);
}

/**
* Close modal for editing category
*/
function closeModal(){
    document.getElementById("edit-cat-modal").style.display="none";
}

/**
* Save changes to category
*/
function saveCat(){
    var name = document.getElementById("edit-cat-header").value;
    var newBudget = document.getElementById("edit-budget-input").value;

    // If user inputs are okay, make AJAX request
    if(verifyInputs(name,newBudget,"category")){
        // Create data for request
        var data;
        data = '{"name":"' + name + '","budget":' + newBudget + '}';

        // Make AJAX request to post new category to category list
        makeReq("PUT", "/budget/cats/"+name, 201, getCats, data);
    }
    document.getElementById("edit-cat-modal").style.display="none";
}

/**
* Delete category
*/
function deleteCat(){
    var name = document.getElementById("edit-cat-header").value;
    makeReq("DELETE", "/budget/cats/"+name, 204, getCats);
    document.getElementById("edit-cat-modal").style.display="none";
}

// setup load event
window.addEventListener("load", setup, true);
