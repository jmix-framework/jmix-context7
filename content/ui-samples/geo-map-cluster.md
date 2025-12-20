<Path>Add-ons > Maps > GeoMap with cluster</Path>

The GeoMap component supports clustering. Any object inside a layer can be grouped into clusters. To enable clustering in VectorLayer, it must contain ClusterSource that has nested DataVectorSource or VectorSource.

geo-map-cluster.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:maps="http://jmix.io/schema/maps/ui">
    <data>
        <collection id="locationsDc"
                    class="io.jmix.uisamples.entity.Location"
                    fetchPlan="_base">
            <loader id="locationsDl">
                <query><![CDATA[select e from Location e]]></query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <maps:geoMap id="map"
                     height="100%"
                     width="100%"
                     minHeight="25em">
            <maps:mapView zoom="14"
                          centerX="-1.9901218933105469"
                          centerY="53.46047450112283"/>
            <maps:layers>
                <maps:tile>
                    <maps:osmSource/>
                </maps:tile>
                <maps:vector>
                    <maps:cluster weightProperty="weight"
                                  distance="30"
                                  minDistance="30">
                        <maps:dataVectorSource dataContainer="locationsDc"
                                               property="point"/>
                    </maps:cluster>
                </maps:vector>
            </maps:layers>
        </maps:geoMap>
    </layout>
</view>



GeoMapClusterSample.java

package io.jmix.uisamples.view.flowui.maps.cluster;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("geo-map-cluster")
@ViewDescriptor("geo-map-cluster.xml")
public class GeoMapClusterSample extends StandardView {
}




Location.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;
import org.locationtech.jts.geom.Point;

import java.util.UUID;

@JmixEntity
@Table(name = "LOCATION")
@Entity(name = "Location")
public class Location {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @Column(name = "NAME")
    private String name;

    @Column(name = "POINT")
    protected Point point;

    @Column(name = "WEIGHT")
    private Integer weight;

    public Integer getWeight() {
        return weight;
    }

    public void setWeight(Integer weight) {
        this.weight = weight;
    }

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

