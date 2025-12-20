<Path>Add-ons > Maps > GeoMap with select mode</Path>

Both `DataVectorSource` and `VectorSource` have a selection mode. To enable selection mode, set the `featureSelectEnabled` attribute to `true`. These sources provide:
- Methods for programmatically selecting and deselecting items, which start with `select` and `deselect`.
- A select event to handle user or programmatic item selection.


geo-map-select-mode.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:maps="http://jmix.io/schema/maps/ui">
    <data>
        <collection id="markersDc" class="io.jmix.uisamples.entity.Marker">
            <loader id="markersDl" readOnly="true"/>
            <fetchPlan extends="_base"/>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <hbox width="100%" height="100%">
            <dataGrid id="mountainsDataGrid"
                      selectionMode="MULTI"
                      dataContainer="markersDc"
                      minHeight="20em"
                      height="100%"
                      width="20em">
                <columns>
                    <column property="name"/>
                </columns>
            </dataGrid>
            <maps:geoMap id="map"
                         width="100%"
                         height="100%"
                         minHeight="25em">
                <maps:mapView centerX="84.51333"
                              centerY="25.88139"
                              zoom="4"/>
                <maps:layers>
                    <maps:tile>
                        <maps:osmSource/>
                    </maps:tile>
                    <maps:vector id="vectorLayer">
                        <maps:dataVectorSource id="source"
                                               featureSelectEnabled="true"
                                               dataContainer="markersDc"
                                               property="point"/>
                    </maps:vector>
                </maps:layers>
            </maps:geoMap>
        </hbox>
    </layout>
</view>



GeoMapSelectModeSample.java

package io.jmix.uisamples.view.flowui.maps.select;

import com.vaadin.flow.data.selection.SelectionEvent;
import io.jmix.core.LoadContext;
import io.jmix.flowui.component.grid.DataGrid;
import io.jmix.flowui.view.*;
import io.jmix.mapsflowui.component.model.source.DataVectorSource;
import io.jmix.mapsflowui.component.model.source.HasGeoObjectSelect.GeoObjectSelectEvent;
import io.jmix.mapsflowui.kit.component.model.style.Fill;
import io.jmix.mapsflowui.kit.component.model.style.Style;
import io.jmix.mapsflowui.kit.component.model.style.image.Anchor;
import io.jmix.mapsflowui.kit.component.model.style.image.IconStyle;
import io.jmix.mapsflowui.kit.component.model.style.text.TextStyle;
import io.jmix.uisamples.bean.MountainService;
import io.jmix.uisamples.entity.Marker;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

@ViewController(id = "geo-map-select-mode")
@ViewDescriptor(path = "geo-map-select-mode.xml")
public class GeoMapSelectModeSample extends StandardView {

    @ViewComponent
    private DataGrid<Marker> mountainsDataGrid;

    @ViewComponent("map.vectorLayer.source")
    private DataVectorSource<Marker> source;

    @Autowired
    private MountainService mountainService;

    @Subscribe
    public void onInit(final InitEvent event) {
        source.setAttributions(List.of("<a href=\"https://www.flaticon.com/free-icons/rocky-mountains\"" +
                " target=\"_blank\">Icons from Flaticon.</a>"));
    }

    @Install(to = "markersDl", target = Target.DATA_LOADER)
    private List<Marker> markersDlLoadDelegate(final LoadContext loadContext) {
        return mountainService.fetchMountains();
    }

    @Install(to = "map.vectorLayer.source", subject = "styleProvider")
    private Style mapVectorLayerSourceStyleProvider(final Marker marker) {
        return new Style()
                .withImage(new IconStyle()
                        .withSrc("icons/maps/mountain.png")
                        .withAnchor(new Anchor(0.5, 0.95))
                        .withScale(0.085))
                .withText(new TextStyle()
                        .withText(marker.getName())
                        .withOffsetY(5)
                        .withFont("bold 15px sans-serif"));
    }

    @Install(to = "map.vectorLayer.source", subject = "selectStyleProvider")
    private List<Style> mapVectorLayerSourceSelectStyleProvider(final Marker marker) {
        return List.of(
                new Style()
                        .withImage(new IconStyle()
                                .withSrc("icons/maps/mountain-selected.png")
                                .withAnchor(new Anchor(0.5, 0.95))
                                .withScale(0.085))
                        .withText(new TextStyle()
                                .withText(marker.getName())
                                .withOffsetY(5)
                                .withFill(new Fill("#024C68"))
                                .withFont("bold 15px sans-serif"))
        );
    }

    @Subscribe("map.vectorLayer.source")
    public void onSourceGeoObjectSelect(final GeoObjectSelectEvent<Marker> event) {
        if (event.isFromClient()) {
            mountainsDataGrid.deselectAll();
            mountainsDataGrid.select(source.getSelectedGeoObjects());
        }
    }

    @Subscribe("mountainsDataGrid")
    public void onMountainsDataGridSelection(final SelectionEvent<DataGrid<Marker>, Marker> event) {
        if (event.isFromClient()) {
            source.deselectAllGeoObjects();
            source.selectGeoObjects(event.getAllSelectedItems());
        }
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



MountainService.java

package io.jmix.uisamples.bean;

import io.jmix.core.Metadata;
import io.jmix.maps.utils.GeometryUtils;
import io.jmix.uisamples.entity.Marker;
import org.springframework.stereotype.Component;

import java.util.List;

@Component("uisamples_MountainService")
public class MountainService {

    private final Metadata metadata;

    public MountainService(Metadata metadata) {
        this.metadata = metadata;
    }

    public List<Marker> fetchMountains() {
        return List.of(
                createMarker("Everest", 86.92528, 27.98806),
                createMarker("K2", 76.51333, 35.88139),
                createMarker("Kangchenjunga", 88.14750, 27.70333),
                createMarker("Lhotse", 86.93306, 27.96167),
                createMarker("Makalu", 87.08889, 27.88972),
                createMarker("Cho Oyu", 86.66083, 28.09417),
                createMarker("Dhaulagiri I", 83.49306, 28.69667),
                createMarker("Manaslu", 84.55972, 28.55),
                createMarker("Nanga Parbat", 74.58917, 35.23722),
                createMarker("Annapurna I", 83.82028, 28.59556)
        );
    }

    private Marker createMarker(String name, double x, double y) {
        Marker marker = metadata.create(Marker.class);
        marker.setName(name);
        marker.setPoint(GeometryUtils.createPoint(x, y));
        return marker;
    }
}


