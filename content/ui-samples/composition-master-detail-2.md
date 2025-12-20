<Path>Cookbook > Compositions > Master-detail at bottom</Path>


This sample illustrates how to reduce the nesting of dialog windows by using master-detail lists of entities at the bottom level of the composition.

Here you can see the same data structure consisting of `Airport`, `Terminal` and `MeetingPoint` entities as in the [2-levels composition]({contextPath}/sample/composition-2-levels) example. But the list of meeting points is displayed next to the list of terminals right in the airport detail view. This master-detail structure eliminates one level of nested dialog windows, thereby improving the user experience.

Implementation details:

- [Airport.java]({currentPath}?tab=Airport.java)
  - `Airport.terminals` attribute is annotated with `@Composition`.

- [Terminal.java]({currentPath}?tab=Terminal.java)
    - `Terminal.meetingPoints` attribute is annotated with `@Composition`.

- [airport-detail-view.xml]({currentPath}?tab=airport-detail-view.xml) shows an airport and the master-detail lists of its terminals and meeting points. 
  - The fetch plan for loading `Airport` contains the `Airport.terminals` attribute which in turn contains `Terminal.meetingPoints`.
  - Two nested collection data containers are defined: for `Airport.terminals` and `Terminal.meetingPoints` attributes.
  - Data grids displaying terminals and meeting points are connected to the respective data containers.
  - The `create` and `edit` actions of the terminals and meeting points data grids open detail views in dialog windows (see `<property name="openMode" value="DIALOG"/>`).

**CAUTION**: In this example, the airport detail view immediately loads nested collections of all terminals and all meeting points of the edited airport. This may affect performance if the nested collections are large.


Airport.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.Composition;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;

import java.util.List;
import java.util.UUID;

@JmixEntity
@Table(name = "AIRPORT", indexes = {
        @Index(name = "IDX_AIRPORT_CITY", columnList = "CITY_ID")
})
@Entity
public class Airport {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @Column(name = "VERSION", nullable = false)
    @Version
    private Integer version;

    @InstanceName
    @Column(name = "NAME", nullable = false)
    @NotNull
    private String name;

    @Column(name = "IATA", length = 3)
    private String iata;

    @JoinColumn(name = "CITY_ID")
    @ManyToOne(fetch = FetchType.LAZY)
    private City city;

    @Composition
    @OrderBy("name")
    @OneToMany(mappedBy = "airport")
    private List<Terminal> terminals;

    public Integer getVersion() {
        return version;
    }

    public void setVersion(Integer version) {
        this.version = version;
    }

    public City getCity() {
        return city;
    }

    public void setCity(City city) {
        this.city = city;
    }

    public String getIata() {
        return iata;
    }

    public void setIata(String iata) {
        this.iata = iata;
    }

    public List<Terminal> getTerminals() {
        return terminals;
    }

    public void setTerminals(List<Terminal> terminals) {
        this.terminals = terminals;
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




Terminal.java

package io.jmix.uisamples.entity;

import io.jmix.core.DeletePolicy;
import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.entity.annotation.OnDeleteInverse;
import io.jmix.core.metamodel.annotation.Composition;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;

import java.util.List;
import java.util.UUID;

@JmixEntity
@Table(name = "TERMINAL", indexes = {
        @Index(name = "IDX_TERMINAL_AIRPORT", columnList = "AIRPORT_ID")
})
@Entity
public class Terminal {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @Column(name = "VERSION", nullable = false)
    @Version
    private Integer version;

    @InstanceName
    @Column(name = "NAME", nullable = false)
    @NotNull
    private String name;

    @OnDeleteInverse(DeletePolicy.CASCADE)
    @JoinColumn(name = "AIRPORT_ID", nullable = false)
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    private Airport airport;

    @Column(name = "TERMINAL_TYPE", length = 1)
    private String terminalType;

    @Column(name = "GATE_COUNT")
    private Integer gateCount;

    @Composition
    @OrderBy("name")
    @OneToMany(mappedBy = "terminal")
    private List<MeetingPoint> meetingPoints;

    public TerminalType getTerminalType() {
        return terminalType == null ? null : TerminalType.fromId(terminalType);
    }

    public void setTerminalType(TerminalType terminalType) {
        this.terminalType = terminalType == null ? null : terminalType.getId();
    }

    public Integer getGateCount() {
        return gateCount;
    }

    public void setGateCount(Integer gateCount) {
        this.gateCount = gateCount;
    }

    public List<MeetingPoint> getMeetingPoints() {
        return meetingPoints;
    }

    public void setMeetingPoints(List<MeetingPoint> meetingPoints) {
        this.meetingPoints = meetingPoints;
    }

    public Airport getAirport() {
        return airport;
    }

    public void setAirport(Airport airport) {
        this.airport = airport;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getVersion() {
        return version;
    }

    public void setVersion(Integer version) {
        this.version = version;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }
}




MeetingPoint.java

package io.jmix.uisamples.entity;

import io.jmix.core.DeletePolicy;
import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.entity.annotation.OnDeleteInverse;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;

import java.util.UUID;

@JmixEntity
@Table(name = "MEETING_POINT", indexes = {
        @Index(name = "IDX_MEETING_POINT_TERMINAL", columnList = "TERMINAL_ID")
})
@Entity
public class MeetingPoint {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @Column(name = "VERSION", nullable = false)
    @Version
    private Integer version;

    @InstanceName
    @Column(name = "NAME", nullable = false)
    @NotNull
    private String name;

    @Column(name = "DESCRIPTION")
    private String description;

    @OnDeleteInverse(DeletePolicy.CASCADE)
    @JoinColumn(name = "TERMINAL_ID", nullable = false)
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    private Terminal terminal;

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Terminal getTerminal() {
        return terminal;
    }

    public void setTerminal(Terminal terminal) {
        this.terminal = terminal;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getVersion() {
        return version;
    }

    public void setVersion(Integer version) {
        this.version = version;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }
}




airport-detail-view.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      title="msg://airportDetailView.title"
      focusComponent="form">
    <data>
        <instance id="airportDc"
                  class="io.jmix.uisamples.entity.Airport">
            <fetchPlan extends="_base">
                <property name="city" fetchPlan="_base"/>
                <property name="terminals" fetchPlan="_base">
                    <property name="meetingPoints" fetchPlan="_base"/>
                </property>
            </fetchPlan>
            <loader id="airportDl"/>
            <collection id="terminalsDc" property="terminals">
                <collection id="meetingPointsDc" property="meetingPoints"/>
            </collection>
        </instance>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <actions>
        <action id="saveAction" type="detail_saveClose"/>
        <action id="closeAction" type="detail_close"/>
    </actions>
    <layout>
        <formLayout id="form" dataContainer="airportDc">
            <responsiveSteps>
                <responsiveStep minWidth="0" columns="1"/>
                <responsiveStep minWidth="40em" columns="2"/>
            </responsiveSteps>
            <textField id="nameField" property="name"/>
            <textField id="iataField" property="iata"/>
            <entityComboBox id="cityField" property="city">
                <actions>
                    <action id="entityClear" type="entity_clear"/>
                </actions>
                <itemsQuery class="io.jmix.uisamples.entity.City" escapeValueForLike="true"
                            searchStringFormat="(?i)%${inputString}%">
                    <fetchPlan extends="_base"/>
                    <query>
                        <![CDATA[select e from City e where e.name like :searchString escape '\' order by e.name]]>
                    </query>
                </itemsQuery>
            </entityComboBox>
        </formLayout>
        <hbox width="100%">
            <vbox padding="false">
                <h4 text="msg://io.jmix.uisamples.entity/Airport.terminals"/>
                <hbox id="buttonsPanel" classNames="buttons-panel">
                    <button action="terminalsDataGrid.create"/>
                    <button action="terminalsDataGrid.edit"/>
                    <button action="terminalsDataGrid.remove"/>
                </hbox>
                <dataGrid id="terminalsDataGrid" dataContainer="terminalsDc" width="100%" minHeight="10em">
                    <actions>
                        <action id="create" type="list_create">
                            <properties>
                                <property name="openMode" value="DIALOG"/>
                                <property name="viewId" value="terminal-detail-1"/>
                            </properties>
                        </action>
                        <action id="edit" type="list_edit">
                            <properties>
                                <property name="openMode" value="DIALOG"/>
                                <property name="viewId" value="terminal-detail-1"/>
                            </properties>
                        </action>
                        <action id="remove" type="list_remove"/>
                    </actions>
                    <columns>
                        <column property="name" editable="true"/>
                        <column property="terminalType" editable="true"/>
                        <column property="gateCount" editable="true"/>
                    </columns>
                </dataGrid>
            </vbox>
            <vbox padding="false">
                <h4 text="msg://io.jmix.uisamples.entity/Terminal.meetingPoints"/>
                <hbox id="meetingPointsButtonsPanel" classNames="buttons-panel">
                    <button action="meetingPointsDataGrid.create"/>
                    <button action="meetingPointsDataGrid.edit"/>
                    <button action="meetingPointsDataGrid.remove"/>
                </hbox>
                <dataGrid id="meetingPointsDataGrid" dataContainer="meetingPointsDc" width="100%" minHeight="10em">
                    <actions>
                        <action id="create" type="list_create">
                            <properties>
                                <property name="openMode" value="DIALOG"/>
                                <property name="viewId" value="meeting-point-detail-4"/>
                            </properties>
                        </action>
                        <action id="edit" type="list_edit">
                            <properties>
                                <property name="openMode" value="DIALOG"/>
                                <property name="viewId" value="meeting-point-detail-4"/>
                            </properties>
                        </action>
                        <action id="remove" type="list_remove"/>
                    </actions>
                    <columns>
                        <column property="name"/>
                        <column property="description"/>
                    </columns>
                </dataGrid>
            </vbox>
        </hbox>
        <hbox id="detailActions">
            <button id="saveAndCloseButton" action="saveAction"/>
            <button id="closeButton" action="closeAction"/>
        </hbox>
    </layout>
</view>




AirportDetailView.java

package io.jmix.uisamples.view.flowui.cookbook.composition4;

import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Airport;

@ViewController(id = "airport-detail-4")
@ViewDescriptor(path = "airport-detail-view.xml")
@EditedEntityContainer("airportDc")
@DialogMode(width = "64em", resizable = true)
public class AirportDetailView extends StandardDetailView<Airport> {
}




terminal-detail-view.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      title="msg://terminalDetailView.title"
      focusComponent="form">
    <data>
        <instance id="terminalDc"
                  class="io.jmix.uisamples.entity.Terminal">
            <fetchPlan extends="_base"/>
            <loader id="terminalDl"/>
        </instance>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <actions>
        <action id="saveAction" type="detail_saveClose"/>
        <action id="closeAction" type="detail_close"/>
    </actions>
    <layout>
        <formLayout id="form" dataContainer="terminalDc">
            <responsiveSteps>
                <responsiveStep minWidth="0" columns="1"/>
                <responsiveStep minWidth="40em" columns="2"/>
            </responsiveSteps>
            <textField id="nameField" property="name"/>
            <select id="terminalTypeField" property="terminalType"/>
            <textField id="gateCountField" property="gateCount"/>
        </formLayout>
        <hbox id="detailActions">
            <button id="saveAndCloseButton" action="saveAction"/>
            <button id="closeButton" action="closeAction"/>
        </hbox>
    </layout>
</view>




TerminalDetailView.java

package io.jmix.uisamples.view.flowui.cookbook.composition4;

import io.jmix.flowui.view.EditedEntityContainer;
import io.jmix.flowui.view.StandardDetailView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.Terminal;

@ViewController(id = "terminal-detail-4")
@ViewDescriptor(path = "terminal-detail-view.xml")
@EditedEntityContainer("terminalDc")
public class TerminalDetailView extends StandardDetailView<Terminal> {
}




meeting-point-detail-view.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      title="msg://meetingPointDetailView.title"
      focusComponent="form">
    <data>
        <instance id="meetingPointDc"
                  class="io.jmix.uisamples.entity.MeetingPoint">
            <fetchPlan extends="_base"/>
            <loader id="meetingPointDl"/>
        </instance>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <actions>
        <action id="saveAction" type="detail_saveClose"/>
        <action id="closeAction" type="detail_close"/>
    </actions>
    <layout>
        <formLayout id="form" dataContainer="meetingPointDc">
            <responsiveSteps>
                <responsiveStep minWidth="0" columns="1"/>
                <responsiveStep minWidth="40em" columns="2"/>
            </responsiveSteps>
            <textField id="nameField" property="name"/>
            <textField id="descriptionField" property="description"/>
        </formLayout>
        <hbox id="detailActions">
            <button id="saveAndCloseButton" action="saveAction"/>
            <button id="closeButton" action="closeAction"/>
        </hbox>
    </layout>
</view>




MeetingPointDetailView.java

package io.jmix.uisamples.view.flowui.cookbook.composition4;

import io.jmix.flowui.view.EditedEntityContainer;
import io.jmix.flowui.view.StandardDetailView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.MeetingPoint;

@ViewController(id = "meeting-point-detail-4")
@ViewDescriptor(path = "meeting-point-detail-view.xml")
@EditedEntityContainer("meetingPointDc")
public class MeetingPointDetailView extends StandardDetailView<MeetingPoint> {
}


