<Path>Add-ons > Maps > GeoMap with modify style</Path>

The modify styles apply not to the feature's geometry but to the generated vertex points of the feature's geometry. Thus, the created style should be applicable to the `Point` geometry. The modify styles can be set:
- Globally, using the layer's modify styles.
- Individually for specific features.

Note, modify styles will be applied when the `featureModifyEnabled` attribute in the vector source is set to `true` and modify mode is activated.


geo-map-modify-style.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:maps="http://jmix.io/schema/maps/ui">
    <layout>
        <div classNames="rounded-panel">
            <span text="msg://sampleDescription.text"/>
        </div>
        <maps:geoMap id="map"
                     width="100%"
                     height="100%"
                     minHeight="25em">
            <maps:mapView centerX="-20"
                          centerY="5"
                          zoom="2.1"/>
            <maps:layers>
                <maps:tile>
                    <maps:osmSource/>
                </maps:tile>
                <maps:vector id="vectorLayer">
                    <maps:vectorSource id="source" featureModifyEnabled="true"/>
                </maps:vector>
            </maps:layers>
        </maps:geoMap>
    </layout>
</view>



GeoMapModifyStyleSample.java

package io.jmix.uisamples.view.flowui.maps.modifystyle;

import io.jmix.flowui.view.*;
import io.jmix.mapsflowui.component.model.feature.LineStringFeature;
import io.jmix.mapsflowui.component.model.feature.PolygonFeature;
import io.jmix.mapsflowui.component.model.layer.VectorLayer;
import io.jmix.mapsflowui.component.model.source.VectorSource;
import io.jmix.mapsflowui.kit.component.model.feature.FeatureType;
import io.jmix.mapsflowui.kit.component.model.layer.LayerStylesBuilder;
import io.jmix.mapsflowui.kit.component.model.style.Fill;
import io.jmix.mapsflowui.kit.component.model.style.PointStyle;
import io.jmix.mapsflowui.kit.component.model.style.Style;
import io.jmix.mapsflowui.kit.component.model.style.image.CircleStyle;
import io.jmix.mapsflowui.kit.component.model.style.stroke.Stroke;

import java.util.List;

@ViewController(id = "geo-map-modify-style")
@ViewDescriptor(path = "geo-map-modify-style.xml")
public class GeoMapModifyStyleSample extends StandardView {

    @ViewComponent("map.vectorLayer")
    private VectorLayer vectorLayer;
    @ViewComponent("map.vectorLayer.source")
    private VectorSource source;

    @Subscribe
    public void onInit(final InitEvent event) {
        source.addAllFeatures(List.of(
                createLineStringWithModifyStyle(),
                createPolygonWithModifyStyle(),
                new LineStringFeature(Geometries.createLineString()),
                new PolygonFeature(Geometries.createPolygon())
        ));

        setupGeneralModifyStyle();
    }

    private void setupGeneralModifyStyle() {
        Style generalStyle = new PointStyle()
                .withImage(new CircleStyle()
                        .withRadius(8)
                        .withFill(new Fill("blue")))
                .build();

        vectorLayer.setModifyStyles(LayerStylesBuilder.modifyStyles(false)
                .withStyles(FeatureType.POLYGON, List.of(generalStyle))
                .withStyles(FeatureType.LINE_STRING, List.of(generalStyle))
                .build());
    }

    private LineStringFeature createLineStringWithModifyStyle() {
        return new LineStringFeature(Geometries.createLineStringStyled())
                .withModifyStyles(new PointStyle()
                        .withImage(new CircleStyle()
                                .withRadius(6)
                                .withFill(new Fill("red"))
                                .withStroke(new Stroke()
                                        .withWidth(2d)
                                        .withColor("green")))
                        .build());
    }

    private PolygonFeature createPolygonWithModifyStyle() {
        return new PolygonFeature(Geometries.createPolygonStyled())
                .withModifyStyles(new PointStyle()
                        .withImage(new CircleStyle()
                                .withRadius(7)
                                .withFill(new Fill("#63ADD0")))
                        .build());
    }
}



Geometries.java

package io.jmix.uisamples.view.flowui.maps.modifystyle;

import io.jmix.maps.utils.GeometryUtils;
import org.locationtech.jts.geom.*;

public final class Geometries {

    private static final GeometryFactory factory = GeometryUtils.getGeometryFactory();

    public static LineString createLineString() {
        return factory.createLineString(
                new Coordinate[]{
                        new Coordinate(-25.0, 45.0),
                        new Coordinate(-30.0, 40.0),
                        new Coordinate(-25.0, 35.0),
                        new Coordinate(-30.0, 30.0),
                        new Coordinate(-25.0, 25.0),
                        new Coordinate(-30.0, 20.0),
                        new Coordinate(-25.0, 15.0),
                        new Coordinate(-30.0, 10.0)
                }
        );
    }

    public static LineString createLineStringStyled() {
        return factory.createLineString(
                new Coordinate[]{
                        new Coordinate(-45.0, 45.0),
                        new Coordinate(-50.0, 40.0),
                        new Coordinate(-45.0, 35.0),
                        new Coordinate(-50.0, 30.0),
                        new Coordinate(-45.0, 25.0),
                        new Coordinate(-50.0, 20.0),
                        new Coordinate(-45.0, 15.0),
                        new Coordinate(-50.0, 10.0)
                }
        );
    }

    public static Polygon createPolygon() {
        return factory.createPolygon(factory.createLinearRing(
                new Coordinate[]{
                        new Coordinate(-15, 45),
                        new Coordinate(0, 45),
                        new Coordinate(0, 35),
                        new Coordinate(-15, 35),
                        new Coordinate(-15, 45),
                }));
    }

    public static Polygon createPolygonStyled() {
        return factory.createPolygon(factory.createLinearRing(
                new Coordinate[]{
                        new Coordinate(-15, 10),
                        new Coordinate(-15, 30),
                        new Coordinate(10, 30),
                        new Coordinate(10, 10),
                        new Coordinate(-15, 10),
                }));
    }
}


