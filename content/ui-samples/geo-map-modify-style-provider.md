<Path>Add-ons > Maps > GeoMap with modify style provider</Path>

The `DataVectorSource` provides the ability to set a modify style generator to generate styles for each geo-object on the source.

The modify styles apply not to the feature's geometry but to the generated vertex points of the feature's geometry. Thus, the created style should be applicable to the `Point` geometry.

Note, select styles will be applied when the `featureSelectEnabled` attribute in the vector source is set to `true`.


geo-map-modify-style-provider.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
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
        <div classNames="border rounded-s p-s">
            <span text="msg://sampleDescription.text"/>
        </div>
        <maps:geoMap id="map"
                     width="100%"
                     height="100%"
                     minHeight="25em">
            <maps:mapView centerX="18.045731051682072"
                          centerY="49.63906914590179"
                          zoom="3.6"/>
            <maps:layers>
                <maps:tile>
                    <maps:osmSource/>
                </maps:tile>
                <maps:vector id="vectorLayer">
                    <maps:dataVectorSource id="source"
                                           featureModifyEnabled="true"
                                           dataContainer="markersDc"
                                           property="point"/>
                </maps:vector>
            </maps:layers>
        </maps:geoMap>
    </layout>
</view>



GeoMapModifyStyleProviderSample.java

package io.jmix.uisamples.view.flowui.maps.modifystyleprovider;

import io.jmix.flowui.view.*;
import io.jmix.mapsflowui.kit.component.model.style.Fill;
import io.jmix.mapsflowui.kit.component.model.style.PointStyle;
import io.jmix.mapsflowui.kit.component.model.style.Style;
import io.jmix.mapsflowui.kit.component.model.style.image.CircleStyle;
import io.jmix.mapsflowui.kit.component.model.style.stroke.Stroke;
import io.jmix.uisamples.entity.Marker;

import java.util.List;
import java.util.Map;

@ViewController(id = "geo-map-modify-style-provider")
@ViewDescriptor(path = "geo-map-modify-style-provider.xml")
public class GeoMapModifyStyleProviderSample extends StandardView {

    private final Map<String, String> cityColors = Map.of(
            "Moscow", "#1531AE",
            "Helsinki", "#589800",
            "Berlin", "#8C003D",
            "Paris", "#A67500",
            "London", "#034769"
    );

    @Install(to = "map.vectorLayer.source", subject = "modifyStyleProvider")
    private List<Style> mapVectorLayerSourceModifyStyleProvider(final Marker marker) {
        return List.of(new PointStyle()
                .withImage(new CircleStyle()
                        .withRadius(10)
                        .withFill(new Fill(cityColors.get(marker.getName())))
                        .withStroke(new Stroke()
                                .withWidth(2d)
                                .withColor("#ffffff")))
                .build());
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

