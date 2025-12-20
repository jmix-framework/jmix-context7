<Path>Add-ons > Maps > GeoMap with custom projection</Path>

This example demonstrates how to set a custom projection with its corresponding coordinate reference system.

To add a custom projection, a [`ProjectionRegistration`]({currentPath}?tab=UiSamplesMapsConfiguration.java) bean must be created. It should contain the name of the projection and its definition in the `PROJ.4` format.


geo-map-custom-projection.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:maps="http://jmix.io/schema/maps/ui">
    <layout>
        <maps:geoMap id="map" height="100%" width="100%" minHeight="20em">
            <maps:mapView projection="EPSG:27700" zoom="4.5" centerX="530000" centerY="180000"/>
            <maps:layers>
                <maps:tile>
                    <maps:osmSource/>
                </maps:tile>
                <maps:vector id="vectorLayer">
                    <maps:vectorSource id="source"/>
                </maps:vector>
            </maps:layers>
        </maps:geoMap>
    </layout>
</view>




GeoMapCustomProjectionSample.java

package io.jmix.uisamples.view.flowui.maps.projection;

import io.jmix.flowui.view.*;
import io.jmix.maps.utils.GeometryUtils;
import io.jmix.mapsflowui.component.GeoMap;
import io.jmix.mapsflowui.component.model.feature.MarkerFeature;
import io.jmix.mapsflowui.component.model.source.VectorSource;

@ViewController(id = "geo-map-custom-projection")
@ViewDescriptor(path = "geo-map-custom-projection.xml")
public class GeoMapCustomProjectionSample extends StandardView {

    @ViewComponent
    private GeoMap map;

    @ViewComponent("map.vectorLayer.source")
    private VectorSource source;

    @Subscribe
    public void onInit(final InitEvent event) {
        map.setProjection(() -> "EPSG:27700");

        source.addFeature(new MarkerFeature(GeometryUtils.createPoint(530000, 180000)));
    }
}




UiSamplesMapsConfiguration.java

package io.jmix.uisamples;

import io.jmix.mapsflowui.component.projection.GeoMapProjectionRegistration;
import io.jmix.mapsflowui.component.projection.ProjectionRegistration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class UiSamplesMapsConfiguration {

    @Bean
    public ProjectionRegistration epsg27700() {
        return new GeoMapProjectionRegistration("EPSG:27700",
                       """
                        +proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 +x_0=400000 +y_0=-100000 +ellps=airy
                        +towgs84=446.448,-125.157,542.06,0.15,0.247,0.842,-20.489
                        +units=m +no_defs
                        """);
    }
}


