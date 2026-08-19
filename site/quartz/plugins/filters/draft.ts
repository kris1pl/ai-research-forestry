import { QuartzFilterPlugin } from "../types"

export const RemoveDrafts: QuartzFilterPlugin<{}> = () => ({
  name: "RemoveDrafts",
  shouldPublish(_ctx, [_tree, vfile]) {
    const fm = vfile.data?.frontmatter ?? {}
    const draftFlag: boolean = fm.draft === true || fm.draft === "true"
    const statusDraft = fm.status === "draft"
    return !draftFlag && !statusDraft
  },
})
