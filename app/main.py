from __future__ import print_function
from google.refine import refine
import pandas as pd


class RefineServerHelper:
    def __init__(self, refine_server):
        self.refine_server = refine_server

    def list_projects(self):
        """
        List OpenRefine projects
        """
        projects = {
            k: v for k, v in self.refine_server.list_projects().items() if v is not None
        }
        return (
            pd.DataFrame(projects)
            .transpose()
            .reset_index()
            .rename({"index": "ProjectId"}, axis=1)
        )

    def search_projects(self, project_name):
        """
        Search OpenRefine project by name
        """
        t = self.list_projects()
        if t.shape[0] > 0:
            t = t[t.name == project_name]
        return t

    def delete_project_byname(self, project_name):
        """
        Delete OpenRefine project by name
        """
        t = self.search_projects(project_name)
        for x in t.ProjectId.values:
            if self.refine_server.open_project(project_id=x).delete():
                print("Project {} deleted".format(x), end="\n\n")

    def open_project_byname(self, project_name, project_id=None):
        """
        Open openrefine project by name
        """
        if project_id == None:
            t = self.search_projects(project_name)
            if t.shape[0] == 0:
                raise Exception(
                    "No instance with Project Name: '{}' exist".format(
                        project_name, t.loc[:, ["ProjectId", "Project Name"]]
                    )
                )
            if t.shape[0] > 1:
                raise Exception(
                    "More than one instance with Project Name: '{}'\n{}\nPlease specify the project id".format(
                        project_name, t.loc[:, ["ProjectId", "Project Name"]]
                    )
                )
            project_id = t.ProjectId.values[0]
        else:
            project_name = refine_server.get_project_name(project_id)
        self.active_project = self.refine_server.open_project(project_id)
        print(
            "OpenRefine Project '{}' opened, access using active_project property".format(
                project_name
            )
        )
        return self.active_project

    def get_number_columns(self):
        return len(self.active_project.columns)

    def get_number_rows(self):
        return self.active_project.get_rows().total

    def get_rows(self, start=0, limit=10):
        temp_rows = []
        for x in self.active_project.get_rows(
            start=start, limit=limit
        ).rows.rows_response:
            temp_cells = []
            for y_t in self.active_project.get_models()["columnModel"]["columns"]:
                y = x["cells"][y_t["cellIndex"]]
                if y != None:
                    temp_cells.append(y["v"])
                else:
                    temp_cells.append(None)
            temp_rows.append(temp_cells)
        return pd.DataFrame(temp_rows, columns=self.active_project.columns)

    def to_lowercase(self, column_name):
        return self.active_project.text_transform(
            column=column_name, expression="value.toLowercase()"
        )

    def to_uppercase(self, column_name):
        return self.active_project.text_transform(
            column=column_name, expression="value.toUppercase()"
        )

    def to_titlecase(self, column_name):
        return self.active_project.text_transform(
            column=column_name, expression="value.toTitlecase()"
        )

    # def cluster(self,column_name,cluster_type="binning",function=None,params=None):
    #     return pd.DataFrame(drug_project.compute_clusters(column_name,cluster_type,function,params))


if __name__ == "__main__":
    print(refine.RefineServer().get_version(), end="\n\n")

    refine_server = refine.Refine(refine.RefineServer())
    refine_helper = RefineServerHelper(refine_server)
    # print(refine_helper.list_projects().to_string(), end="\n\n")

    refine_helper.delete_project_byname("wine")
    wine_project = refine_server.new_project(
        project_file="/app/data/wine-raw.csv", project_name="wine", separator=","
    )

    # print(refine_helper.search_projects("wine").iloc[0].to_string(), end="\n\n")
    refine_helper.open_project_byname("wine")
    print("Fields: {}".format([x.encode("utf-8") for x in wine_project.columns]))
    print(
        "Dimensions: [{rows}, {cols}]".format(
            rows=refine_helper.get_number_rows(),
            cols=refine_helper.get_number_columns(),
        ),
        end="\n\n",
    )

    print(refine_helper.get_rows(start=0, limit=1).iloc[0].to_string(), end="\n\n")
