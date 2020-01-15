/* Magic Mirror Config Sample
 *
 * By Michael Teeuw http://michaelteeuw.nl
 * MIT Licensed.
 */

var config = {
    port: 8080,

    language: 'en',
    timeFormat: 24,
    units: 'metric',

    modules: [
    {
        module: 'aiclient',
        position: 'middle_center' // This can be any of the regions.
    },
    {
        module: 'aiclientdebugger',
        position: 'bottom_right'
    },
    {
        module: "newsfeed",
        position: "bottom_bar",
        config: {
            feeds: [
                {
                    title: "New York Times",
                    url: "http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml"
                }
            ],
            showSourceTitle: true,
            showPublishDate: true,
            broadcastNewsFeeds: true,
            broadcastNewsUpdates: true
        }
    },
    {
        module: "currentweather",
        position: "top_right",
        config: {
            // ID from http://bulk.openweathermap.org/sample/city.list.json.gz; unzip the gz file and find your city
            location: "",
            locationID: "",
            appid: "",
            units: "metric",
            degreeLabel: true
        }
    },
    {
        module: "clock",
        position: "top_left",
        config: {
            "timeFormat": 12
        }
    },
    ]

};

/*************** DO NOT EDIT THE LINE BELOW ***************/
if (typeof module !== 'undefined') {module.exports = config;}
