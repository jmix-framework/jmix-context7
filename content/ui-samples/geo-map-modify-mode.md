<Path>Add-ons > Maps > GeoMap with modify mode</Path>

Both `DataVectorSource` and `VectorSource` have a modify mode. To enable modify mode, set the `featureModifyEnabled` attribute to `true`. These sources provide modify start and modify end events.

Additionally, `VectorSource` provides the `SourceFeatureDeleteEvent`.


geo-map-modify-mode.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:maps="http://jmix.io/schema/maps/ui">
    <layout>
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



GeoMapModifyModeSample.java

package io.jmix.uisamples.view.flowui.maps.modify;

import com.vaadin.flow.component.notification.Notification;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.view.*;
import io.jmix.mapsflowui.component.model.feature.LineStringFeature;
import io.jmix.mapsflowui.component.model.feature.PolygonFeature;
import io.jmix.mapsflowui.component.model.source.HasFeatureDelete.SourceFeatureDeleteEvent;
import io.jmix.mapsflowui.component.model.source.HasFeatureModify.SourceFeatureModifyEndEvent;
import io.jmix.mapsflowui.component.model.source.HasFeatureModify.SourceFeatureModifyStartEvent;
import io.jmix.mapsflowui.component.model.source.VectorSource;
import io.jmix.mapsflowui.kit.component.model.feature.Feature;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController(id = "geo-map-modify-mode")
@ViewDescriptor(path = "geo-map-modify-mode.xml")
public class GeoMapModifyModeSample extends StandardView {

    @Autowired
    private Notifications notifications;

    @ViewComponent("map.vectorLayer.source")
    private VectorSource source;

    @Subscribe
    public void onInit(final InitEvent event) {
        source.addFeature(new LineStringFeature(Geometries.createLineString())
                .withProperty("name", "LineString"));
        source.addFeature(new PolygonFeature(Geometries.createPolygon())
                .withProperty("name", "Polygon"));
    }

    @Subscribe("map.vectorLayer.source")
    public void onSourceFeatureModifyStart(final SourceFeatureModifyStartEvent event) {
        Feature feature = event.getFeatures().iterator().next();
        notifications.create("ModifyStartEvent",
                        "Feature: " + feature.getProperties().get("name"))
                .withPosition(Notification.Position.BOTTOM_END)
                .show();
    }

    @Subscribe("map.vectorLayer.source")
    public void onSourceFeatureModifyEnd(final SourceFeatureModifyEndEvent event) {
        Feature feature = event.getFeatures().iterator().next();
        notifications.create("ModifyEndEvent",
                        "Feature: " + feature.getProperties().get("name"))
                .withPosition(Notification.Position.BOTTOM_END)
                .show();
    }

    @Subscribe("map.vectorLayer.source")
    public void onSourceFeatureDelete(final SourceFeatureDeleteEvent event) {
        Feature feature = event.getFeatures().iterator().next();
        notifications.create("DeleteEvent",
                        "Feature: " + feature.getProperties().get("name"))
                .withPosition(Notification.Position.BOTTOM_END)
                .show();
    }
}



Geometries.java

package io.jmix.uisamples.view.flowui.maps.modify;

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
}


