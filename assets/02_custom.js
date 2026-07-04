window.dash_clientside = Object.assign({}, window.dash_clientside, {
    lottie: {
        load: function(animation_data, element_id) {

            if (!animation_data) {
                return "";
            }

            const container =
                document.getElementById(element_id);

            if (!container) {
                return "";
            }

            container.innerHTML = "";

            lottie.loadAnimation({
                container: container,
                renderer: "svg",
                loop: true,
                autoplay: true,
                animationData: animation_data
            });

            return "";
        }
    }
});