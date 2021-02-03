var ViewModel = function () {
    var self = this;
    self.url = window.location.href
    self.users = ko.observableArray([]);
    self.userCount = ko.observable(0);
    self.tableClass = ko.observable("d-none");
    self.filterFirst = ko.observable();
    self.filterLast = ko.observable();
    self.filterAge = ko.observable();
    self.filterCountry = ko.observable();
    self.filterUState = ko.observable();
    var apigateway = "APGATEWAY";
    var tableVis = "container overflow-auto contentbox w-75";
    
    var displayValue = function(element, valueAccessor){
        var value = ko.utils.unwrapObservable(valueAccessor());
        var isCurrentlyVisible = !(element.style.display == "none");
        if(value && !isCurrentlyVisible)
        element.style.display = "";
        else if((!value) && isCurrentlyVisible)
        element.style.display = "none";
    };


    ko.bindingHandlers['loading-animation'] = {

        'init' : function(element, valueAccessor){
        $(element)
                .append(
                    '<div class="circle circle1 circle1-1"><div class="circle circle1 circle2-1"><div class="circle circle1 circle3-1"></div></div></div>');

        displayValue(element, valueAccessor);
        },
        'update' : function(element, valueAccessor){
        displayValue(element, valueAccessor);
        }
    };

    IsLoading = ko.observable(true);

    self.filterUsers = function() {
        var filterData = {
            "name.\"first\"": self.filterFirst(),
            "name.\"last\"": self.filterLast(),
            "dob.age": self.filterAge(),
            "location.country": self.filterCountry(),
            "location.state": self.filterUState(),
        };
        fetch(apigateway+'?filters='+JSON.stringify(filterData))
        .then(response => response.json())
        .then(data => self.users(data));
    };

    fetch(apigateway)
        .then(response => response.json())
        .then(data => self.users(data));
    

    setInterval(function() {
        self.userCount(self.users().length)
        if (self.users().length > 0) {
            IsLoading(false);
            self.tableClass(tableVis);
        }
    }, 3000);
    
  };

ko.applyBindings(new ViewModel());