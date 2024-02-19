"use strict";

// Class definition
var KTMapsWidget2 = (function () {
    // Private methods
    var initMap = function () {
        // Check if amchart library is included
        if (typeof am5 === 'undefined') {
            return;
        }

        var element = document.getElementById("kt_maps_widget_2_map");

        if (!element) {
            return;
        }

        // Root
        var root;

        var init = function() {
            // Create root element
            // https://www.amcharts.com/docs/v5/getting-started/#Root_element
            root = am5.Root.new(element);

            // Set themes
            // https://www.amcharts.com/docs/v5/concepts/themes/
            root.setThemes([am5themes_Animated.new(root)]);

            // Create the map chart
            // https://www.amcharts.com/docs/v5/charts/map-chart/
            var chart = root.container.children.push(
                am5map.MapChart.new(root, {
                    panX: "translateX",
                    panY: "translateY",
                    projection: am5map.geoOrthographic(),
                    paddingLeft: 0,
                    paddingRight: 0,
                    paddingBottom: 0,
                    rotationX: -74,
                    rotationY: -25,
                })
            );

            // Load Tamil Nadu GeoJSON data
            fetch('/static/assets/js/TamilNadu.geojson')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to load Tamil Nadu GeoJSON data; status:', response.status);
                    }
                    return response.json();
                })
                .then(tamilNaduGeoJSON => {
                    // Create a new MapPolygonSeries for Tamil Nadu district borders
                    var tnDistrictsSeries = chart.series.push(
                        am5map.MapPolygonSeries.new(root, {
                            // Use the loaded GeoJSON data
                            geoJSON: tamilNaduGeoJSON,
                        })
                    );

                    // Customize appearance of the district borders
                    tnDistrictsSeries.mapPolygons.template.setAll({
                        fill: am5.color("rgba(0, 0, 0, 0)"), // Make the borders transparent initially
                        stroke: am5.color("red"), // Customize the border color
                        strokeWidth: 1, // Customize the border width
                        tooltipText: "{NAME_2}", // Display district name as tooltip
                    });

                    // Show district borders on hover
                    tnDistrictsSeries.mapPolygons.template.states.create("hover", {
                        fill: am5.color("rgba(0, 0, 0, 0.2)"), // Semi-transparent fill color on hover
                    });

                    // Show district borders on click
                    tnDistrictsSeries.mapPolygons.template.events.on("hit", function (event) {
                        event.target.isActive = !event.target.isActive;
                    });
                })
                .catch(error => {
                    console.error(error);
                });

            // Set clicking on "water" to zoom out
            chart.chartContainer
                .get("background")
                .events.on("click", function () {
                    chart.goHome();
                });

            // Make stuff animate on load
            chart.appear(1000, 100);
        };

        // On amchart ready
        am5.ready(function () {
            init();
        }); // end am5.ready()

        // Update chart on theme mode change
        KTThemeMode.on("kt.thememode.change", function() {     
            // Destroy chart
            root.dispose();

            // Reinit chart
            init();
        });
    };

    // Public methods
    return {
        init: function () {
            initMap();
        },
    };
})();

// Webpack support
if (typeof module !== "undefined") {
    module.exports = KTMapsWidget2;
}

// On document ready
KTUtil.onDOMContentLoaded(function () {
    KTMapsWidget2.init();
});
