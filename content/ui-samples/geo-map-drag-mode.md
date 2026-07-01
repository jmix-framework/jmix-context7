<Path>Add-ons > Maps > GeoMap with drag mode</Path>

Both `DataVectorSource` and `VectorSource` have a drag mode. To enable drag mode, set the `featureDragEnabled` attribute to `true`. These sources provide drag start and drag end events.


geo-map-drag-mode.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:maps="http://jmix.io/schema/maps/ui">
    <data>
        <collection id="markersDc" class="io.jmix.uisamples.entity.Marker">
            <loader id="markersDl" readOnly="true">
                <query>
                    <![CDATA[select e from Marker e]]>
                </query>
            </loader>
            <fetchPlan extends="_base"/>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <div classNames="rounded-panel">
            <span text="msg://sampleDescription.text"/>
        </div>
        <maps:geoMap id="map"
                     width="100%"
                     height="100%"
                     minHeight="25em">
            <maps:mapView centerX="18.045731051682072"
                          centerY="50.83906914590179"
                          zoom="3.6"/>
            <maps:layers>
                <maps:tile>
                    <maps:osmSource/>
                </maps:tile>
                <maps:vector id="vectorLayer">
                    <maps:dataVectorSource id="source"
                                           featureDragEnabled="true"
                                           dataContainer="markersDc"
                                           property="point"/>
                </maps:vector>
            </maps:layers>
        </maps:geoMap>
    </layout>
</view>



GeoMapDragModeSample.java

package io.jmix.uisamples.view.flowui.maps.drag;

import com.vaadin.flow.component.notification.Notification;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.view.*;
import io.jmix.mapsflowui.component.model.source.HasGeoObjectDrag.GeoObjectDragEndEvent;
import io.jmix.mapsflowui.component.model.source.HasGeoObjectDrag.GeoObjectDragStartEvent;
import io.jmix.uisamples.entity.Marker;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController(id = "geo-map-drag-mode")
@ViewDescriptor(path = "geo-map-drag-mode.xml")
public class GeoMapDragModeSample extends StandardView {

    @Autowired
    private Notifications notifications;

    @Subscribe("map.vectorLayer.source")
    public void onSourceGeoObjectDragStart(final GeoObjectDragStartEvent<Marker> event) {
        Marker marker = event.getItems().iterator().next();
        notifications.create("DragStartEvent", marker.getName())
                .withPosition(Notification.Position.BOTTOM_END)
                .show();
    }

    @Subscribe("map.vectorLayer.source")
    public void onSourceGeoObjectDragEnd(final GeoObjectDragEndEvent<Marker> event) {
        Marker marker = event.getItems().iterator().next();
        notifications.create("DragEndEvent", marker.getName())
                .withPosition(Notification.Position.BOTTOM_END)
                .show();
    }
}



Marker.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import org.locationtech.jts.geom.Point;

import java.util.UUID;

@JmixEntity
@Table(name = "MARKER")
@Entity
public class Marker {
    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @InstanceName
    @Column(name = "NAME")
    private String name;

    @Column(name = "POINT")
    private Point point;

    public Point getPoint() {
        return point;
    }

    public void setPoint(Point point) {
        this.point = point;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }
}

