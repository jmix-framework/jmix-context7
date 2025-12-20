<Path>Add-ons > Maps > GeoMap with points</Path>

Users can place points on the map. To display points from JPA or DTO entity is used DataVectorSource. It binds with data container via dataContainer and property attributes. Property must have Point datatype or any other supported by GeoMap component. By default, all points from data container are displayed with blue marker. If it is needed to display points that not related wth JPA or DTO, the VectorSource can be used. This source provides methods to add/remove features of any type.

geo-map-point.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:maps="http://jmix.io/schema/maps/ui">
    <data>
        <collection id="markersDc"
                    class="io.jmix.uisamples.entity.Marker"
                    fetchPlan="_base">
            <loader id="markersDl">
                <query><![CDATA[select e from Marker e]]></query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <maps:geoMap id="map"
                     width="100%"
                     height="100%"
                     minHeight="25em">
            <maps:mapView centerX="18.045731051682072"
                          centerY="51.83906914590179"
                          zoom="3.6"/>
            <maps:layers>
                <maps:tile>
                    <maps:osmSource/>
                </maps:tile>
                <maps:vector id="dataLayer">
                    <maps:dataVectorSource id="dataSource" dataContainer="markersDc" property="point"/>
                </maps:vector>
                <maps:vector id="vectorLayer">
                    <maps:vectorSource id="vectorSource"/>
                </maps:vector>
            </maps:layers>
        </maps:geoMap>
    </layout>
</view>




GeoMapPointSample.java

package io.jmix.uisamples.view.flowui.maps.point;

import com.vaadin.flow.component.notification.Notification;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.view.*;
import io.jmix.mapsflowui.component.model.feature.PointFeature;
import io.jmix.mapsflowui.component.model.source.DataVectorSource;
import io.jmix.mapsflowui.component.model.source.GeoObjectClickNotifier;
import io.jmix.mapsflowui.component.model.source.SourceFeatureClickNotifier;
import io.jmix.mapsflowui.component.model.source.VectorSource;
import io.jmix.uisamples.entity.Marker;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

import static io.jmix.maps.utils.GeometryUtils.createPoint;

@ViewController("geo-map-point")
@ViewDescriptor("geo-map-point.xml")
public class GeoMapPointSample extends StandardView {

    @Autowired
    private Notifications notifications;

    @ViewComponent("map.dataLayer.dataSource")
    private DataVectorSource<Marker> dataSource;

    @ViewComponent("map.vectorLayer.vectorSource")
    private VectorSource vectorSource;

    @Subscribe
    public void onInit(final InitEvent event) {
        dataSource.addGeoObjectClickListener(this::onDataVectorSourceClick);
        vectorSource.addSourceFeatureClickListener(this::onVectorSourceClick);

        vectorSource.addAllFeatures(List.of(
                new PointFeature(createPoint(30.327877976068475, 59.94327979807139)),
                new PointFeature(createPoint(13.722223426393388, 51.05181869560283)),
                new PointFeature(createPoint(-2.2449710026111562, 53.47839876123808))
        ));
    }

    private void onVectorSourceClick(SourceFeatureClickNotifier.SourceFeatureClickEvent event) {
        notifications.create("GeoObjectClickEvent", ((PointFeature) event.getFeature()).getPoint().toText())
                .withPosition(Notification.Position.BOTTOM_END)
                .show();
    }

    private void onDataVectorSourceClick(GeoObjectClickNotifier.GeoObjectClickEvent<Marker> event) {
        notifications.create("GeoObjectClickEvent", event.getItem().getPoint().toText())
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

