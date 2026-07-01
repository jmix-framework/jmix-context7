<Path>Cookbook > Data in UI > Cascading dropdowns</Path>

Cascading dropdowns filter their items based on the previous selection in a hierarchy. This example shows how to implement selection of two dependent entities: Planets and their Moons. When the user selects a planet in the first dropdown, the second dropdown shows the moons of the selected planet. Entities are loaded into two data containers: planetsDc and moonsDc. The loader query of the moons container has the :container_planetsDc parameter, which refers to the planets container by its name. This parameter is recognized by the DataLoadCoordinator facet, which automatically reloads the moons container each time the selected value in the planets container changes. The onPlanetsComboBoxValueChange() handler clears the current value of the moons dropdown when the selected planet changes.

cascading-dropdowns.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <collection id="planetsDc"
                    class="io.jmix.uisamples.entity.Planet"
                    fetchPlan="_base">
            <loader>
                <query>
                    <![CDATA[select p from Planet p
                    where (select count(m) from Moon m where m.planet = p) > 0
                    order by p.id]]>
                </query>
            </loader>
        </collection>
        <collection id="moonsDc"
                    class="io.jmix.uisamples.entity.Moon"
                    fetchPlan="_base">
            <loader>
                <query>
                    <![CDATA[select m from Moon m where m.planet = :container_planetsDc order by m.name]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout classNames="horizontal-layout">
        <entityComboBox id="planetsComboBox" label="Planets" metaClass="Planet" itemsContainer="planetsDc"/>
        <entityComboBox id="moonsComboBox" label="Moons" metaClass="Moon" itemsContainer="moonsDc"/>
    </layout>
</view>




CascadingDropdownsSample.java

package io.jmix.uisamples.view.flowui.cookbook.cascadingdropdowns;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import io.jmix.flowui.component.combobox.EntityComboBox;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Moon;
import io.jmix.uisamples.entity.Planet;

@ViewController("cascading-dropdowns")
@ViewDescriptor("cascading-dropdowns.xml")
public class CascadingDropdownsSample extends StandardView {

    @ViewComponent
    protected EntityComboBox<Moon> moonsComboBox;

    @Subscribe("planetsComboBox")
    protected void onPlanetsComboBoxValueChange(ComponentValueChangeEvent<EntityComboBox<Planet>, Planet> event) {
        moonsComboBox.clear();
    }
}




Planet.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;

@Table(name = "PLANET")
@Entity
@JmixEntity
public class Planet {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private Integer id;

    @InstanceName
    @Column(name = "NAME", nullable = false)
    @NotNull
    private String name;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }
}



Moon.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;

@Table(name = "MOON", indexes = {
        @Index(name = "IDX_MOON_PLANET_ID", columnList = "PLANET_ID")
})
@Entity
@JmixEntity
public class Moon {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private Integer id;

    @InstanceName
    @Column(name = "NAME", nullable = false)
    @NotNull
    private String name;

    @JoinColumn(name = "PLANET_ID", nullable = false)
    @NotNull
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    private Planet planet;

    public Planet getPlanet() {
        return planet;
    }

    public void setPlanet(Planet planet) {
        this.planet = planet;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }
}


