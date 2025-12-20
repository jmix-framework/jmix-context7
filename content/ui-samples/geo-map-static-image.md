<Path>Add-ons > Maps > GeoMap with static image</Path>

The GeoMap supports displaying static images as a map content. There is an image layer that can display single images. It contains the following sources: imageStaticSource displays static images. The url attribute defines the URL of external or application resource (see Vaadin docs :: Loading Resources) The source also supports programmatically setting an image using StreamResource. imageWmsSource displays single, untiled images from WMS services. In this example, GeoMap displays image from application resources. Note, that imageStaticSource and mapView must define projection and extent.

geo-map-static-image.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:maps="http://jmix.io/schema/maps/ui">
    <layout>
        <maps:geoMap id="map"
                     width="100%"
                     height="100%"
                     minHeight="25em">
            <maps:mapView centerX="256" centerY="128">
                <maps:projection code="my-static-image"
                                 units="PIXELS">
                    <maps:extent minX="-0" minY="0" maxX="512" maxY="512"/>
                </maps:projection>
            </maps:mapView>
            <maps:layers>
                <maps:image>
                    <maps:imageStaticSource url="icons/icon.png">
                        <maps:projection code="my-static-image"/>
                        <maps:imageExtent minX="0" minY="0" maxX="512" maxY="512"/>
                    </maps:imageStaticSource>
                </maps:image>
            </maps:layers>
        </maps:geoMap>
    </layout>
</view>




GeoMapStaticImageSample.java

package io.jmix.uisamples.view.flowui.maps.staticimage;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("geo-map-static-image")
@ViewDescriptor("geo-map-static-image.xml")
public class GeoMapStaticImageSample extends StandardView {
}


