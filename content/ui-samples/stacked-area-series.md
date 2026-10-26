<Path>Add-ons > Charts > Series > Line series > Stacked Area series</Path>

Series that are in the same stack will be drawn on top of each other. The stack property determines the name of the stack where the current series will set. The stackStrategy property determines how to stack values when the stack property is set. Available options: SAME_SIGN - only stack values if the value to be stacked has the same sign as the currently cumulated stacked value. ALL - stack all values, irrespective of the signs of the current or cumulative stacked value. POSITIVE - only stack positive values. NEGATIVE - only stack negative values.

stacked-area-series.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <data readOnly="true">
        <collection id="transportDc" class="io.jmix.uisamples.entity.TransportCount"
                    fetchPlan="_local">
            <loader id="transportDl" readOnly="true">
                <query>
                    <![CDATA[select e from TransportCount e order by e.year]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em">
            <charts:title text="Traffic incidents" left="0" top="0"/>
            <charts:tooltip trigger="AXIS">
                <charts:formatterFunction>
                    <![CDATA[
                        function (params) {
                              var tar = params[1];

                              return '<b>Year:</b> ' + tar.name + '<br/><hr/>' +
                              '<b>Cars:</b> ' + tar.value.cars + '<br/>' +
                              '<b>Motorcycles:</b> ' + tar.value.motorcycles + '<br/>' +
                              '<b>Bicycles:</b> ' + tar.value.bicycles + '<br/>';
                            }
                    ]]>
                </charts:formatterFunction>
                <charts:axisPointer type="SHADOW"/>
            </charts:tooltip>
            <charts:legend orientation="VERTICAL" right="0" top="40%" unselectedSeries="Cars" />

            <charts:dataZoom>
                <charts:sliderDataZoom orientation="HORIZONTAL" top="5%"/>
            </charts:dataZoom>

            <charts:xAxes>
                <charts:xAxis/>
            </charts:xAxes>
            <charts:yAxes>
                <charts:yAxis/>
            </charts:yAxes>

            <charts:dataSet>
                <charts:source dataContainer="transportDc"
                               categoryField="year" valueFields="cars motorcycles bicycles"/>
            </charts:dataSet>

            <charts:series>
                <charts:line name="Cars" stack="stack">
                    <charts:areaStyle/>
                </charts:line>
                <charts:line name="Motorcycles" stack="stack">
                    <charts:areaStyle/>
                </charts:line>
                <charts:line name="Bicycles" stack="stack">
                    <charts:areaStyle/>
                </charts:line>
            </charts:series>
        </charts:chart>
    </layout>
</view>




StackedAreaSample.java

package io.jmix.uisamples.view.flowui.charts.series.line.stackedarea;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("stacked-area-series")
@ViewDescriptor("stacked-area-series.xml")
public class StackedAreaSample extends StandardView {
}




TransportCount.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;

import java.util.UUID;

@Table(name = "TRANSPORT_COUNT")
@Entity
@JmixEntity
public class TransportCount {

    @Id
    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    private UUID id;

    @NotNull
    @Column(name = "YEAR_", nullable = false)
    private Integer year;

    @NotNull
    @Column(name = "CARS", nullable = false)
    private Integer cars;

    @NotNull
    @Column(name = "MOTORCYCLES", nullable = false)
    private Integer motorcycles;

    @NotNull
    @Column(name = "BICYCLES", nullable = false)
    private Integer bicycles;

    public Integer getBicycles() {
        return bicycles;
    }

    public void setBicycles(Integer bicycles) {
        this.bicycles = bicycles;
    }

    public Integer getMotorcycles() {
        return motorcycles;
    }

    public void setMotorcycles(Integer motorcycles) {
        this.motorcycles = motorcycles;
    }

    public Integer getCars() {
        return cars;
    }

    public void setCars(Integer cars) {
        this.cars = cars;
    }

    public Integer getYear() {
        return year;
    }

    public void setYear(Integer year) {
        this.year = year;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }
}


