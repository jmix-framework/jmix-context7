<Path>Add-ons > Maps > GeoMap with heatmap</Path>

The GeoMap component supports heat maps. A heatmap overlay is intended to display data density distribution across different geo-points. Data density is highlighted with color. By default, regions with higher points density are displayed in red and regions with lower density - in green. In this example first heatmap layer gets the data from data container and second heatmap layer gets data programmatically in a view controller.

geo-map-heatmap.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:maps="http://jmix.io/schema/maps/ui">
    <data>
        <collection id="heatPointsDc"
                    class="io.jmix.uisamples.entity.HeatPoint"
                    fetchPlan="_base">
            <loader id="heatPointsDl">
                <query><![CDATA[select e from HeatPoint e]]></query>
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
                <maps:heatmap weightProperty="intensity"
                              blur="15"
                              radius="20">
                    <maps:heatmapDataVectorSource dataContainer="heatPointsDc"
                                                  property="point"/>
                </maps:heatmap>
                <maps:heatmap id="heatmapLayer"
                              blur="15"
                              maxZoom="15.5"
                              radius="20"
                              weightProperty="weight">
                    <maps:vectorSource id="source"/>
                </maps:heatmap>
            </maps:layers>
        </maps:geoMap>
    </layout>
</view>



GeoMapHeatmapSample.java

package io.jmix.uisamples.view.flowui.maps.heatmap;

import io.jmix.flowui.view.*;
import io.jmix.mapsflowui.component.model.feature.PointFeature;
import io.jmix.mapsflowui.component.model.source.VectorSource;

import java.util.Arrays;
import java.util.Random;
import java.util.stream.Collectors;

import static io.jmix.maps.utils.GeometryUtils.createPoint;

@ViewController("geo-map-heatmap")
@ViewDescriptor("geo-map-heatmap.xml")
public class GeoMapHeatmapSample extends StandardView {

    private static final Random random = new Random();

    @ViewComponent("map.heatmapLayer.source")
    private VectorSource source;

    @Subscribe
    public void onInit(final InitEvent event) {
        source.addAllFeatures(
                Arrays.stream(HeatPoints.getSecondCoordinates())
                        .map(c -> new PointFeature(createPoint(c.getX(), c.getY()))
                                .withProperty("weight", random.nextDouble(0.1, 1)))
                        .collect(Collectors.toList()));
    }
}




HeatPoint.java

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
@Table(name = "HEAT_POINT")
@Entity
public class HeatPoint {
    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @InstanceName
    @Column(name = "NAME")
    private String name;

    @Column(name = "POINT")
    private Point point;

    @Column(name = "INTENSITY")
    private Double intensity;

    public Double getIntensity() {
        return intensity;
    }

    public void setIntensity(Double intensity) {
        this.intensity = intensity;
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

