document.addEventListener("DOMContentLoaded", function () {
  const mapSelector = document.querySelectorAll("#mapOne");

  if (mapSelector.length) {
      const mapOne = new jsVectorMap({
          selector: "#mapOne",
          map: "us_aea_en",
          zoomButtons: true,

          regionStyle: {
              initial: {
                  fill: "#C8D0D8",
              },
              hover: {
                  fillOpacity: 1,
                  fill: "#3056D3",
              },
          },
          regionLabelStyle: {
              initial: {
                  fontFamily: "Satoshi",
                  fontWeight: "semibold",
                  fill: "#fff",
              },
              hover: {
                  cursor: "pointer",
              },
          },

          labels: {
              regions: {
                  render: function (code) {
                      return code.split("-")[1];
                  },
              },
          },
      });
  }
});
