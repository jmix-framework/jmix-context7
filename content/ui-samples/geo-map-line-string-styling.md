<Path>Add-ons > Maps > GeoMap with LineString styling</Path>

LineStringFeature provides styling only the line: its color, width, dash, etc. The first linestring does not have styles. The second one has two styles and the last style overlaps the previous one. The LineStringStyle is an optional helper class. It provides methods for styling applicable only for LineString.

geo-map-line-string-styling.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:maps="http://jmix.io/schema/maps/ui">
    <layout>
        <maps:geoMap id="map"
                     width="100%"
                     height="100%"
                     minHeight="25em">
            <maps:mapView centerX="-30" centerY="15"/>
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



GeoMapLineStringStylingSample.java

package io.jmix.uisamples.view.flowui.maps.linestringstyle;

import io.jmix.flowui.view.*;
import io.jmix.mapsflowui.component.model.feature.LineStringFeature;
import io.jmix.mapsflowui.component.model.source.VectorSource;
import io.jmix.mapsflowui.kit.component.model.style.LineStringStyle;
import io.jmix.mapsflowui.kit.component.model.style.stroke.Stroke;

import java.util.List;

import static io.jmix.maps.utils.GeometryUtils.createLineString;

@ViewController("geo-map-line-string-styling")
@ViewDescriptor("geo-map-line-string-styling.xml")
public class GeoMapLineStringStylingSample extends StandardView {

    @ViewComponent("map.vectorLayer.source")
    private VectorSource source;

    @Subscribe
    public void onInit(final InitEvent event) {
        source.addAllFeatures(List.of(
                new LineStringFeature(createLineString(LineStringCoordinates.getFirstCoordinates())),
                createStyledLineString()
        ));
    }

    private LineStringFeature createStyledLineString() {
        return new LineStringFeature(createLineString(LineStringCoordinates.getSecondCoordinates()))
                .withStyles(
                        new LineStringStyle()
                                .withStroke(new Stroke()
                                        .withWidth(6d)
                                        .withColor("#39E639")
                                        .withLineDash(List.of(20d, 10d)))
                                .build(),
                        new LineStringStyle()
                                .withStroke(new Stroke()
                                        .withWidth(3d)
                                        .withColor("#FF4040")
                                        .withLineDash(List.of(20d, 10d)))
                                .build());
    }
}




LineStringCoordinates.java

package io.jmix.uisamples.view.flowui.maps.linestringstyle;

import org.locationtech.jts.geom.Coordinate;

public final class LineStringCoordinates {

    public static Coordinate[] getFirstCoordinates() {
        return new Coordinate[]{
            new Coordinate(-45.0, 45.0),
            new Coordinate(-50.0, 40.0),
            new Coordinate(-45.0, 35.0),
            new Coordinate(-50.0, 30.0),
            new Coordinate(-45.0, 25.0),
            new Coordinate(-50.0, 20.0),
            new Coordinate(-45.0, 15.0),
            new Coordinate(-50.0, 10.0),
        };
    }

    public static Coordinate[] getSecondCoordinates() {
        return new Coordinate[]{
                new Coordinate(-25.0, 45.0),
                new Coordinate(-30.0, 40.0),
                new Coordinate(-25.0, 35.0),
                new Coordinate(-30.0, 30.0),
                new Coordinate(-25.0, 25.0),
                new Coordinate(-30.0, 20.0),
                new Coordinate(-25.0, 15.0),
                new Coordinate(-30.0, 10.0),
        };
    }
}


