<Path>Cookbook > Compositions > Master-detail on top</Path>


This sample illustrates how to reduce the nesting of dialog windows by using master-detail lists of entities instead of the top level of the composition.

Here you can see the same data structure consisting of `Airport`, `Terminal` and `MeetingPoint` entities as in the [previous example]({contextPath}/sample/composition-2-levels) with two-level relationship. However, the list of terminals is displayed next to the list of airports in a master-detail format, rather than within the airport detail view. This removes one level of nested dialog windows, thereby enhancing the user experience.

In this example, airports and terminals are edited and saved independently, while meeting points are saved to the database only together with the owning terminal. So the composition relationship takes place only for `Terminal` and `MeetingPoint` entities. 

Implementation details: 

- [Airport.java]({currentPath}?tab=Airport.java)
  - `Airport.terminals` attribute is still annotated with `@Composition`, but it doesn't affect the system behavior in this example and can be omitted.

- [Terminal.java]({currentPath}?tab=Terminal.java)
  - `Terminal.meetingPoints` attribute is annotated with `@Composition`.

- [airport-list-view.xml]({currentPath}?tab=airport-list-view.xml)
  - A standalone collection data container is defined for the `Terminal` entity. The list of terminals for the selected airport is loaded into the container by a JPQL query with the `:container_airportsDc` parameter. This parameter is set by the `dataLoadCoordinator` facet in the [automatic mode]({docsBaseUrl}/flow-ui/facets/dataLoadCoordinator.html#automatic-mode).   

- [AirportListView.java]({currentPath}?tab=AirportListView.java)
  - The `terminalsDataGridCreate` action is enabled only when an airport is selected in the airports data grid. The action is initially disabled in [airport-list-view.xml]({currentPath}?tab=airport-list-view.xml).
  - A selected airport is set to a newly created terminal. 

- [terminal-detail-view.xml]({currentPath}?tab=terminal-detail-view.xml)
  - The fetch plan for loading `Terminal` contains the `Terminal.meetingPoints` attribute.
  - A nested collection data container is defined for the `Terminal.meetingPoints` attribute.
  - The data grid displaying meeting points is connected to this data container.
  - The `create` and `edit` actions of the meeting points data grid open the meeting point detail view as a dialog (see `<property name="openMode" value="DIALOG"/>`).


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




airport-list-view.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <collection id="airportsDc"
                    class="io.jmix.uisamples.entity.Airport">
            <fetchPlan extends="_base">
                <property name="city" fetchPlan="_instance_name"/>
            </fetchPlan>
            <loader id="airportsDl" readOnly="true">
                <query>
                    <![CDATA[select e from Airport e order by e.name asc]]>
                </query>
            </loader>
        </collection>
        <collection id="terminalsDc" class="io.jmix.uisamples.entity.Terminal">
            <fetchPlan extends="_base"/>
            <loader id="terminalsDl" readOnly="true">
                <query>
                    <![CDATA[select e from Terminal e where e.airport = :container_airportsDc
                    order by e.name asc]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <hbox width="100%">
            <vbox padding="false">
                <h4 text="msg://airports"/>
                <hbox id="buttonsPanel" classNames="buttons-panel">
                    <button id="createButton" action="airportsDataGrid.create"/>
                    <button id="editButton" action="airportsDataGrid.edit"/>
                    <button id="removeButton" action="airportsDataGrid.remove"/>
                </hbox>
                <dataGrid id="airportsDataGrid"
                              width="100%"
                              minHeight="20em"
                              dataContainer="airportsDc">
                    <actions>
                        <action id="create" type="list_create" actionVariant="DEFAULT">
                            <properties>
                                <property name="openMode" value="DIALOG"/>
                                <property name="viewId" value="airport-detail-3"/>
                            </properties>
                        </action>
                        <action id="edit" type="list_edit">
                            <properties>
                                <property name="openMode" value="DIALOG"/>
                                <property name="viewId" value="airport-detail-3"/>
                            </properties>
                        </action>
                        <action id="remove" type="list_remove"/>
                    </actions>
                    <columns>
                        <column property="name"/>
                        <column property="iata"/>
                        <column property="city"/>
                    </columns>
                </dataGrid>
            </vbox>
            <vbox padding="false">
                <h4 text="msg://terminals"/>
                <hbox id="terminalsButtonsPanel" classNames="buttons-panel">
                    <button id="terminalsCreateButton" action="terminalsDataGrid.create"/>
                    <button id="terminalsEditButton" action="terminalsDataGrid.edit"/>
                    <button id="terminalsRemoveButton" action="terminalsDataGrid.remove"/>
                </hbox>
                <dataGrid id="terminalsDataGrid" dataContainer="terminalsDc" minWidth="100px" width="100%">
                    <actions>
                        <action id="create" type="list_create" actionVariant="DEFAULT" enabled="false">
                            <properties>
                                <property name="openMode" value="DIALOG"/>
                                <property name="viewId" value="terminal-detail-2"/>
                            </properties>
                        </action>
                        <action id="edit" type="list_edit">
                            <properties>
                                <property name="openMode" value="DIALOG"/>
                                <property name="viewId" value="terminal-detail-2"/>
                            </properties>
                        </action>
                        <action id="remove" type="list_remove"/>
                    </actions>
                    <columns>
                        <column property="name"/>
                        <column property="terminalType"/>
                        <column property="gateCount"/>
                    </columns>
                </dataGrid>
            </vbox>
        </hbox>
    </layout>
</view>




AirportListView.java

package io.jmix.uisamples.view.flowui.cookbook.composition3;

import io.jmix.flowui.action.list.CreateAction;
import io.jmix.flowui.model.CollectionContainer;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Airport;
import io.jmix.uisamples.entity.Terminal;

@ViewController(id = "composition-master-detail-1")
@ViewDescriptor(path = "airport-list-view.xml")
@DialogMode(width = "64em")
public class AirportListView extends StandardListView<Airport> {

    @ViewComponent("terminalsDataGrid.create")
    private CreateAction<Terminal> terminalsDataGridCreate;
    @ViewComponent
    private CollectionContainer<Airport> airportsDc;

    @Subscribe(id = "airportsDc", target = Target.DATA_CONTAINER)
    public void onAirportsDcItemChange(final InstanceContainer.ItemChangeEvent<Airport> event) {
        // Enable 'create' action only when there is a selected airport in the data grid
        terminalsDataGridCreate.setEnabled(event.getItem() != null);
    }

    @Install(to = "terminalsDataGrid.create", subject = "initializer")
    private void terminalsDataGridCreateInitializer(final Terminal terminal) {
        // Set the selected airport for a newly created terminal
        terminal.setAirport(airportsDc.getItem());
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
            </fetchPlan>
            <loader id="airportDl"/>
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
        <hbox id="detailActions">
            <button id="saveAndCloseButton" action="saveAction"/>
            <button id="closeButton" action="closeAction"/>
        </hbox>
    </layout>
</view>




AirportDetailView.java

package io.jmix.uisamples.view.flowui.cookbook.composition3;

import io.jmix.flowui.view.EditedEntityContainer;
import io.jmix.flowui.view.StandardDetailView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.Airport;

@ViewController(id = "airport-detail-3")
@ViewDescriptor(path = "airport-detail-view.xml")
@EditedEntityContainer("airportDc")
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
            <fetchPlan extends="_base">
                <property name="meetingPoints" fetchPlan="_base"/>
            </fetchPlan>
            <loader id="terminalDl"/>
            <collection id="meetingPointsDc" property="meetingPoints"/>
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
        <h4 text="msg://io.jmix.uisamples.entity/Terminal.meetingPoints"/>
        <hbox id="buttonsPanel" classNames="buttons-panel">
            <button id="createButton" action="meetingPointsDataGrid.create"/>
            <button id="editButton" action="meetingPointsDataGrid.edit"/>
            <button id="removeButton" action="meetingPointsDataGrid.remove"/>
        </hbox>
        <dataGrid id="meetingPointsDataGrid" dataContainer="meetingPointsDc" width="100%" minHeight="10em">
            <actions>
                <action id="create" type="list_create">
                    <properties>
                        <property name="openMode" value="DIALOG"/>
                        <property name="viewId" value="meeting-point-detail-3"/>
                    </properties>
                </action>
                <action id="edit" type="list_edit">
                    <properties>
                        <property name="openMode" value="DIALOG"/>
                        <property name="viewId" value="meeting-point-detail-3"/>
                    </properties>
                </action>
                <action id="remove" type="list_remove"/>
            </actions>
            <columns>
                <column property="name"/>
                <column property="description"/>
            </columns>
        </dataGrid>
        <hbox id="detailActions">
            <button id="saveAndCloseButton" action="saveAction"/>
            <button id="closeButton" action="closeAction"/>
        </hbox>
    </layout>
</view>




TerminalDetailView.java

package io.jmix.uisamples.view.flowui.cookbook.composition3;

import io.jmix.flowui.view.EditedEntityContainer;
import io.jmix.flowui.view.StandardDetailView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.Terminal;

@ViewController(id = "terminal-detail-3")
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

package io.jmix.uisamples.view.flowui.cookbook.composition3;

import io.jmix.flowui.view.EditedEntityContainer;
import io.jmix.flowui.view.StandardDetailView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.MeetingPoint;

@ViewController(id = "meeting-point-detail-3")
@ViewDescriptor(path = "meeting-point-detail-view.xml")
@EditedEntityContainer("meetingPointDc")
public class MeetingPointDetailView extends StandardDetailView<MeetingPoint> {
}


